# web_complexity_lab/collectors/log_parser.py
from typing import List, Dict, Any
from pathlib import Path
import json


class LogParser:
    """
    Parses test execution logs (JSON step arrays produced by generated tests,
    JUnit XML if present) into normalised per-test timing and status records.

    Expected JSON format (array of step objects):
        [
            {
                "step": 1,
                "action": "click",
                "selector": "...",
                "status": "passed" | "failed",
                "error": "",
                "duration": 0.123,       # seconds
                "url": "...",
                "dom_length": 12345
            },
            ...
        ]
    """

    def __init__(self, app_config):
        self.app_config = app_config

    def collect(self) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        root = Path(self.app_config.root_path)

        # Gather candidate directories from both logs and agents config
        search_dirs: List[Path] = []

        logs_cfg = (
            self.app_config.logs
            if hasattr(self.app_config, "logs") and isinstance(self.app_config.logs, dict)
            else {}
        )
        for rel in logs_cfg.get("junit_paths", []):
            search_dirs.append(root / rel)

        agents_cfg = (
            self.app_config.agents
            if hasattr(self.app_config, "agents") and isinstance(self.app_config.agents, dict)
            else {}
        )
        for rel in agents_cfg.get("log_paths", []):
            search_dirs.append(root / rel)

        for log_dir in search_dirs:
            if not log_dir.exists():
                continue
            for log_file in sorted(log_dir.rglob("*.json")):
                if not log_file.is_file():
                    continue
                parsed = self._parse_json_log(log_file)
                if parsed:
                    results.append(parsed)

        return results

    # ------------------------------------------------------------------
    def _parse_json_log(self, file_path: Path) -> Dict[str, Any] | None:
        """Parse a single JSON test-log file into a normalised record."""
        try:
            content = file_path.read_text(encoding="utf-8")
            data = json.loads(content)
        except (json.JSONDecodeError, OSError):
            return None

        # Accept a bare array of steps or a dict with a "steps" key
        if isinstance(data, list):
            steps = data
        elif isinstance(data, dict) and "steps" in data:
            steps = data["steps"]
        else:
            return None

        if not steps:
            return None

        normalised_steps: List[Dict[str, Any]] = []
        total_duration_s = 0.0
        failures: List[str] = []

        for idx, raw in enumerate(steps):
            dur = raw.get("duration", 0)
            status = raw.get("status", "passed")
            error = raw.get("error", "")
            total_duration_s += dur

            if status == "failed":
                failures.append(error or f"step {idx} failed")

            normalised_steps.append({
                "step_index": idx,
                "duration_ms": round(dur * 1000, 1),
                "status": status,
            })

        total_duration_ms = round(total_duration_s * 1000, 1)
        passed_count = sum(1 for s in normalised_steps if s["status"] == "passed")
        failed_count = len(normalised_steps) - passed_count
        overall_status = "passed" if failed_count == 0 else "failed"

        return {
            "test_id": file_path.stem,
            "status": overall_status,
            "duration_ms": total_duration_ms,
            "steps": normalised_steps,
            "passed_steps": passed_count,
            "failed_steps": failed_count,
            "retries": 0,
            "failures": failures,
        }