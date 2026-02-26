# web_complexity_lab/collectors/test_parser.py
from typing import List, Dict, Any
from pathlib import Path
import re


class TestParser:
    """
    Parses UI tests (Playwright TypeScript and Python) into normalized step representation.
    """

    def __init__(self, app_config):
        self.app_config = app_config

    def collect(self) -> List[Dict[str, Any]]:
        results = []
        test_paths = self.app_config.tests.get("test_paths", [])
        root = Path(self.app_config.root_path)

        for rel_path in test_paths:
            test_dir = root / rel_path
            if not test_dir.exists():
                continue

            # Find all test files
            for test_file in test_dir.rglob("*"):
                if test_file.suffix in [".ts", ".py"] and test_file.is_file():
                    parsed = self._parse_test_file(test_file)
                    if parsed:
                        results.extend(parsed)

        return results

    def _parse_test_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse a single test file and extract test info."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return []

        tests = []

        if file_path.suffix == ".ts":
            tests = self._parse_typescript_tests(content, file_path)
        elif file_path.suffix == ".py":
            tests = self._parse_python_tests(content, file_path)

        return tests

    def _parse_typescript_tests(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Playwright TypeScript test files."""
        tests = []

        # Find test blocks: test('name', ...)
        test_pattern = r"test\s*\(\s*['\"]([^'\"]+)['\"]"
        test_matches = re.findall(test_pattern, content)

        # Count actions in the file
        actions = self._count_actions(content)

        # If we found test names, create entries for each
        if test_matches:
            steps_per_test = max(1, actions["total"] // len(test_matches))
            for test_name in test_matches:
                tests.append({
                    "test_id": test_name.replace(" ", "_").lower(),
                    "file": str(file_path),
                    "framework": "playwright",
                    "steps": self._generate_steps(actions, steps_per_test),
                    "steps_count": steps_per_test,
                    "clicks": actions["clicks"] // max(1, len(test_matches)),
                    "fills": actions["fills"] // max(1, len(test_matches)),
                    "navigations": actions["navigations"] // max(1, len(test_matches)),
                    "assertions": actions["assertions"] // max(1, len(test_matches)),
                })
        elif actions["total"] > 0:
            # No named tests but has actions - treat whole file as one test
            tests.append({
                "test_id": file_path.stem,
                "file": str(file_path),
                "framework": "playwright",
                "steps": self._generate_steps(actions, actions["total"]),
                "steps_count": actions["total"],
                "clicks": actions["clicks"],
                "fills": actions["fills"],
                "navigations": actions["navigations"],
                "assertions": actions["assertions"],
            })

        return tests

    def _parse_python_tests(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Playwright Python test files."""
        tests = []

        # Find test functions: def test_xxx(
        test_pattern = r"def\s+(test_\w+)\s*\("
        test_matches = re.findall(test_pattern, content)

        actions = self._count_actions(content)

        if test_matches:
            steps_per_test = max(1, actions["total"] // len(test_matches))
            for test_name in test_matches:
                tests.append({
                    "test_id": test_name,
                    "file": str(file_path),
                    "framework": "playwright",
                    "steps": self._generate_steps(actions, steps_per_test),
                    "steps_count": steps_per_test,
                    "clicks": actions["clicks"] // max(1, len(test_matches)),
                    "fills": actions["fills"] // max(1, len(test_matches)),
                    "navigations": actions["navigations"] // max(1, len(test_matches)),
                    "assertions": actions["assertions"] // max(1, len(test_matches)),
                })
        elif actions["total"] > 0:
            tests.append({
                "test_id": file_path.stem,
                "file": str(file_path),
                "framework": "playwright",
                "steps": self._generate_steps(actions, actions["total"]),
                "steps_count": actions["total"],
                "clicks": actions["clicks"],
                "fills": actions["fills"],
                "navigations": actions["navigations"],
                "assertions": actions["assertions"],
            })

        return tests

    def _count_actions(self, content: str) -> Dict[str, int]:
        """Count different action types in test content."""
        clicks = len(re.findall(r"\.click\s*\(", content))
        fills = len(re.findall(r"\.fill\s*\(", content))
        types = len(re.findall(r"\.type\s*\(", content))
        gotos = len(re.findall(r"\.goto\s*\(", content))
        navigations = len(re.findall(r"\.navigate\s*\(", content)) + gotos
        assertions = len(re.findall(r"(expect|assert|toBe|toEqual|toBeVisible|toHaveText)", content))
        selects = len(re.findall(r"\.select\s*\(", content))

        total = clicks + fills + types + navigations + selects

        return {
            "clicks": clicks,
            "fills": fills + types,
            "navigations": navigations,
            "assertions": assertions,
            "selects": selects,
            "total": max(1, total),
        }

    def _generate_steps(self, actions: Dict[str, int], count: int) -> List[Dict[str, Any]]:
        """Generate step list based on action counts."""
        steps = []
        for i in range(count):
            step_type = "click"  # default
            if i < actions["navigations"]:
                step_type = "navigate"
            elif i < actions["navigations"] + actions["fills"]:
                step_type = "fill"
            steps.append({"type": step_type, "index": i})
        return steps
