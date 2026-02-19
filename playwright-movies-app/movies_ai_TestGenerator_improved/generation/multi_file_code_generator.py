# generation/multi_file_code_generator.py
import os
from typing import Dict, List, Any


class MultiFileCodeGenerator:
    """
    Generate separate Playwright test files per group:
      - test_movies_menus.py
      - test_movies_navigation.py
      - test_movies_actions.py
    """

    def generate_tests_by_group(
        self,
        grouped_plans: Dict[str, List[Dict[str, Any]]],
        base_url: str,
        output_dir: str,
    ) -> None:
        os.makedirs(output_dir, exist_ok=True)

        for group_name, steps in grouped_plans.items():
            if not steps:
                continue

            filename = f"test_movies_{group_name}.py"
            output_path = os.path.join(output_dir, filename)
            self._write_group_test(group_name, steps, base_url, output_path)
            print(f"Generated {group_name} tests -> {output_path}")

    def _write_group_test(
        self,
        group_name: str,
        steps: List[Dict[str, Any]],
        base_url: str,
        output_path: str,
    ) -> None:
        func_name = f"test_movies_{group_name}"

        lines: List[str] = [
            "from playwright.sync_api import sync_playwright\n",
            "import time\n",
            "\n",
            f"def {func_name}():\n",
            f"    print('=== START {group_name.upper()} TESTS ===')\n",
            "    errors = []\n",
            "    with sync_playwright() as p:\n",
            "        browser = p.chromium.launch(headless=False)\n",
            "        context = browser.new_context()\n",
            "        page = context.new_page()\n",
            f"        page.goto('{base_url}', wait_until='domcontentloaded')\n",
            "        print('Base URL:', page.url)\n",
            "        print('DOM length:', len(page.content()))\n",
            "        time.sleep(0.5)\n\n",
        ]

        for idx, step in enumerate(steps, start=1):
            step_type = step.get("type")
            lines.append(f"        print('\\n--- {group_name} step {idx} ({step_type}) ---')\n")
            lines.append("        try:\n")

            if step_type == "click":
                selector = step["selector"]
                escaped = selector.replace("\\", "\\\\").replace("'", "\\'")
                lines.append(f"            page.click('{escaped}', timeout=5000)\n")
                lines.append(f"            print('CLICK {escaped} OK')\n")
            elif step_type == "scroll":
                amount = step.get("amount", 0)
                lines.append(f"            page.mouse.wheel(0, {amount})\n")
                lines.append(f"            print('SCROLL by {amount}')\n")
            else:
                lines.append("            print('Unknown step type; skipping')\n")

            lines.append("            print('URL:', page.url)\n")
            lines.append("            print('DOM length:', len(page.content()))\n")
            lines.append("        except Exception as e:\n")
            lines.append("            print('ERROR:', e)\n")
            lines.append("            errors.append(str(e))\n")
            lines.append("        time.sleep(0.5)\n\n")

        lines.append("        print('\\n=== FINISHED TESTS ===')\n")
        lines.append("        if errors:\n")
        lines.append("            print('\\nSome steps failed:')\n")
        lines.append("            for err in errors:\n")
        lines.append("                print(err)\n")
        lines.append("        browser.close()\n")
        lines.append("\n")
        lines.append("if __name__ == '__main__':\n")
        lines.append(f"    {func_name}()\n")

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
