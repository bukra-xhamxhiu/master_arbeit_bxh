"""
Baseline exploration agent for the Kanban task-management web app.

This script uses Playwright’s synchronous Python API to navigate the
application, discover interactive elements, and perform simple user
actions while logging each step.
"""

import json
import time
import hashlib
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_URL = "http://localhost:3000"
LOG_PATH = Path("logs/kanban_explore.jsonl")
MAX_STEPS = 100


def fingerprint_state(page) -> str:
    url = page.url
    dom_len = page.evaluate("() => document.documentElement.outerHTML.length")
    data = f"{url}|{dom_len}"
    return hashlib.sha1(data.encode("utf-8")).hexdigest()


def collect_interactables(page):
    candidates = []

    roles = ["button", "link", "checkbox", "textbox", "switch"]
    for role in roles:
        locator = page.get_by_role(role)
        try:
            count = locator.count()
        except Exception:
            count = 0
        for i in range(count):
            el = locator.nth(i)
            try:
                if not el.is_visible():
                    continue
            except Exception:
                continue
            name = (el.inner_text() or "").strip() or (el.get_attribute("aria-label") or "")
            if not name:
                continue
            candidates.append({
                "strategy": "role",
                "role": role,
                "name": name,
                "description": f"{role}:{name}",
            })

    css_locator = page.locator("button, a, [role='button'], [role='link']")
    try:
        count = css_locator.count()
    except Exception:
        count = 0
    for i in range(count):
        el = css_locator.nth(i)
        try:
            if not el.is_visible():
                continue
        except Exception:
            continue
        tag = el.evaluate("el => el.tagName.toLowerCase()")
        text = (el.inner_text() or "").strip()
        css_id = el.get_attribute("id") or ""
        css_classes = el.get_attribute("class") or ""
        if css_id:
            selector = f"#{css_id}"
        else:
            first_class = css_classes.split()[0] if css_classes else ""
            selector = f"{tag}.{first_class}" if first_class else tag
        candidates.append({
            "strategy": "css",
            "selector": selector,
            "description": f"{tag} {text or selector}",
        })

    seen = set()
    unique = []
    for c in candidates:
        key_parts = [c["strategy"]]
        if c["strategy"] == "role":
            key_parts.append(c["role"])
            key_parts.append(c["name"])
        else:
            key_parts.append(c["selector"])
        key = "|".join(key_parts)
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique


def select_action(candidates, visited_actions):
    priority = []
    secondary = []
    for c in candidates:
        desc = c["description"].lower()
        key = json.dumps(c, sort_keys=True)
        if key in visited_actions:
            continue
        if any(k in desc for k in ["add", "create", "new", "edit", "delete"]):
            priority.append(c)
        else:
            secondary.append(c)
    ordered = priority + secondary
    return ordered[0] if ordered else None


def perform_action(page, action):
    if action["strategy"] == "role":
        locator = page.get_by_role(action["role"], name=action["name"])
    else:
        locator = page.locator(action["selector"])
    locator.first.click()


def log_step(log_file, step_idx, page, state_fingerprint, action, status, error=None):
    dom_length = page.evaluate("() => document.documentElement.outerHTML.length")
    entry = {
        "step": step_idx,
        "timestamp": time.time(),
        "url": page.url,
        "dom_length": dom_length,
        "fingerprint": state_fingerprint,
        "action": action,
        "status": status,
        "error": error,
    }
    log_file.write(json.dumps(entry) + "\n")
    log_file.flush()

    if status == "ok":
        print(f"[STEP {step_idx}] OK   | {action['description']} | url={page.url} | dom={dom_length}")
    else:
        print(f"[STEP {step_idx}] FAIL | {action['description']} | error={error}")


def explore():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Writing exploration log to: {LOG_PATH}")
    print(f"Target URL: {BASE_URL}")

    with LOG_PATH.open("w", encoding="utf-8") as log_file:
        with sync_playwright() as p:
            print("Launching browser…")
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            print("Opening application…")
            page.goto(BASE_URL, wait_until="networkidle")

            visited_actions = set()
            step_idx = 0

            while step_idx < MAX_STEPS:
                state_fp = fingerprint_state(page)
                candidates = collect_interactables(page)
                print(f"Step {step_idx}: found {len(candidates)} interactable elements.")

                action = select_action(candidates, visited_actions)
                if action is None:
                    print("No new actions available. Stopping exploration.")
                    break

                visited_actions.add(json.dumps(action, sort_keys=True))
                print(f"Chosen action: {action['description']} (strategy={action['strategy']})")

                try:
                    perform_action(page, action)
                    page.wait_for_timeout(500)
                    log_step(log_file, step_idx, page, state_fp, action, status="ok")
                except Exception as e:
                    log_step(log_file, step_idx, page, state_fp, action, status="error", error=str(e))

                step_idx += 1

            print("Closing browser.")
            browser.close()
            print("Exploration finished.")


if __name__ == "__main__":
    try:
        explore()
    except Exception as e:
        print("FATAL ERROR in explore():", repr(e))
