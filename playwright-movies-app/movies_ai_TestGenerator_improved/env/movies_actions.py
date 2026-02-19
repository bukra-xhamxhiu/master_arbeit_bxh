# env/movies_actions.py
#extracts actionable UI elements from DOM. 
from typing import List, Dict, Any
from playwright.sync_api import Page


def get_menu_items(page: Page) -> List[Dict[str, str]]:
    """
    Heuristic: visible links in header/nav are considered menu items.
    """
    items: List[Dict[str, str]] = []

    nav_links = page.query_selector_all("header a, nav a")
    seen = set()

    for link in nav_links:
        try:
            text = (link.inner_text() or "").strip()
        except Exception:
            text = ""

        href = link.get_attribute("href") or ""

        if not text:
            continue

        key = (text, href)
        if key in seen:
            continue
        seen.add(key)

        selector = f'a:has-text("{text}")'

        items.append({
            "selector": selector,
            "text": text,
            "href": href,
        })

    return items


def get_movie_cards(page: Page, max_cards: int = 5) -> List[Dict[str, str]]:
    """
    Heuristic: try to detect movie cards/links on the main grid.
    """
    cards: List[Dict[str, str]] = []

    # Strategy 1: data-testid-based selectors (used often in Playwright examples)
    locators = page.query_selector_all(
        "[data-testid='movie-card'], "
        "[data-testid='movie-card-link'], "
        "[data-testid='movie-card-title']"
    )

    # Strategy 2: generic movie links in main
    if not locators:
        locators = page.query_selector_all(
            "main a[href*='/movie'], main a[href*='category='], main a[href*='genre=']"
        )

    # Strategy 3: if still nothing, fallback to any link in main
    if not locators:
        locators = page.query_selector_all("main a")

    for i, loc in enumerate(locators):
        if i >= max_cards:
            break

        try:
            text = (loc.inner_text() or "").strip()
        except Exception:
            text = ""

        href = loc.get_attribute("href") or ""

        if href:
            selector = f"a[href='{href}']"
        else:
            selector = "main a"

        cards.append({
            "selector": selector,
            "text": text,
        })

    return cards


def get_theme_toggle_selector(page: Page) -> str | None:
    """
    Try to find a theme toggle button (☀ / ☾).
    """
    buttons = page.query_selector_all("button, [role='button']")
    for btn in buttons:
        try:
            text = (btn.inner_text() or "").strip()
        except Exception:
            text = ""
        if text in ("☀", "☾"):
            return "button:has-text(\"" + text + "\")"
    return None


def create_click_action(selector: str, group: str) -> Dict[str, Any]:
    return {"type": "click", "selector": selector, "group": group}
