# generation/playwright_code_generator.py
import os
import json
from typing import List, Dict, Any


class PlaywrightCodeGenerator:
    """
    Generate a Playwright Python test that:
      - replays the given test plan,
      - prints detailed logs to the console,
      - saves a JSON log file with per-step execution data into ../logs
        (i.e. the logs directory inside playwright_ai).
    """

    def generate_python_test(
        self,
        test_plan: List[Dict[str, Any]],
        output_path: str,
        base_url: str = "http://127.0.0.1:5500/dist/index.html",
    ) -> None:
        lines: List[str] = []

        lines.extend(
            [
                "from playwright.sync_api import sync_playwright\n",
                "import time\n",
                "import os\n",
                "import json\n",
                "\n",
                "def _write_json_log(test_name, step_results):\n",
                "    \"\"\"Write step_results as JSON into ../logs/<test_name>.json\"\"\"\n",
                "    # __file__ points to tests/generated/test_*.py\n",
                "    root_dir = os.path.dirname(os.path.dirname(__file__))  # .../playwright_ai\n",
                "    logs_dir = os.path.join(root_dir, 'logs')\n",
                "    os.makedirs(logs_dir, exist_ok=True)\n",
                "    log_path = os.path.join(logs_dir, f'{test_name}.json')\n",
                "    with open(log_path, 'w', encoding='utf-8') as f:\n",
                "        json.dump(step_results, f, indent=2)\n",
                "    print(f'JSON log written to: {log_path}')\n",
                "\n",
                "def test_generated_ui():\n",
                "    # Use the filename (without .py) as the name for the JSON log.\n",
                "    test_name = os.path.splitext(os.path.basename(__file__))[0]\n",
                "    step_results = []  # one entry per click step\n",
                "    with sync_playwright() as p:\n",
                "        browser = p.chromium.launch(headless=False)\n",
                "        context = browser.new_context()\n",
                "        page = context.new_page()\n",
                f"        page.goto('{base_url}', wait_until='domcontentloaded')\n",
                "        print('=== START GENERATED COFFEE SHOP TEST ===')\n",
                "        print('Opening base URL...')\n",
                "        print('URL:', page.url)\n",
                "        print('DOM length:', len(page.content()))\n",
                "        time.sleep(0.5)\n",
                "\n",
            ]
        )

        step_index = 1
        for step in test_plan:
            # For now we only handle click actions in the Coffee Shop plan
            if step.get("action") != "click":
                continue

            selector = step["selector"]
            escaped_selector = selector.replace("\\", "\\\\").replace("'", "\\'")
            label = escaped_selector

            lines.append(f"        print('\\n--- Step {step_index}: CLICK {label} ---')\n")
            lines.append(f"        selector = '{escaped_selector}'\n")
            lines.append("        start = time.time()\n")
            lines.append("        try:\n")
            lines.append("            page.click(selector, timeout=5000)\n")
            lines.append("            status = 'passed'\n")
            lines.append("            error = ''\n")
            lines.append("        except Exception as e:\n")
            lines.append("            status = 'failed'\n")
            lines.append("            error = str(e)\n")
            lines.append("        duration = time.time() - start\n")
            lines.append("        url = page.url\n")
            lines.append("        dom_length = len(page.content())\n")
            lines.append("        print('STATUS:', status)\n")
            lines.append("        if error:\n")
            lines.append("            print('ERROR:', error)\n")
            lines.append("        print('New URL:', url)\n")
            lines.append("        print('DOM length:', dom_length)\n")
            lines.append("        step_results.append({\n")
            lines.append("            'step': %d,\n" % step_index)
            lines.append("            'action': 'click',\n")
            lines.append("            'selector': selector,\n")
            lines.append("            'status': status,\n")
            lines.append("            'error': error,\n")
            lines.append("            'duration': duration,\n")
            lines.append("            'url': url,\n")
            lines.append("            'dom_length': dom_length,\n")
            lines.append("        })\n")
            lines.append("        time.sleep(0.5)\n\n")

            step_index += 1

        lines.extend(
            [
                "        print('\\n=== FINISHED GENERATED COFFEE SHOP TEST ===')\n",
                "        _write_json_log(test_name, step_results)\n",
                "        browser.close()\n",
                "\n",
                "if __name__ == '__main__':\n",
                "    test_generated_ui()\n",
            ]
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
