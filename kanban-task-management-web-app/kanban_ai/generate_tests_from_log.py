import json
from pathlib import Path

LOG_PATH = Path("logs/kanban_explore.jsonl")
OUT_TEST_PATH = Path("tests_generated/test_kanban_generated.py")
BASE_URL = "http://localhost:3000"


def load_log():
    steps = []
    if not LOG_PATH.exists():
        raise FileNotFoundError(f"Log file not found: {LOG_PATH}")
    with LOG_PATH.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                steps.append(json.loads(line))
            except json.JSONDecodeError:
                # skip corrupted lines
                continue
    return steps


def action_to_code(step_index, action):
    """
    Turn a logged action into a Playwright line of code.
    """
    comment = f"    # Step {step_index}: {action.get('description', '').replace('#', '').strip()}\n"

    if action["strategy"] == "role":
        role = action["role"]
        name = action["name"].replace('"', '\\"')
        line = f'    page.get_by_role("{role}", name="{name}").click()\n'
    else:
        selector = action["selector"].replace('"', '\\"')
        line = f'    page.locator("{selector}").first.click()\n'

    return comment + line


def generate():
    steps = load_log()

    # Filter out only successful actions
    ok_steps = [s for s in steps if s.get("status") == "ok"]

    if not ok_steps:
        raise RuntimeError("No successful steps found in log; nothing to generate.")

    OUT_TEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUT_TEST_PATH.open("w", encoding="utf-8") as f:
        f.write("from playwright.sync_api import Page\n\n\n")
        f.write(f'BASE_URL = "{BASE_URL}"\n\n\n')
        f.write("def test_generated_kanban_flow(page: Page):\n")
        f.write('    page.goto(BASE_URL, wait_until="networkidle")\n\n')

        for s in ok_steps:
            step_idx = s.get("step", 0)
            action = s["action"]
            f.write(action_to_code(step_idx, action))

        # simple sanity check at the end
        f.write("\n")
        f.write("    # Basic smoke assertion: page is still on the app\n")
        f.write('    assert "http://localhost:3000" in page.url\n')

    print(f"Generated test file: {OUT_TEST_PATH}")


if __name__ == "__main__":
    generate()
