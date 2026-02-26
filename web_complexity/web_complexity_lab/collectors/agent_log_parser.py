# web_complexity_lab/collectors/agent_log_parser.py
from typing import List, Dict, Any
from pathlib import Path
import json


class AgentLogParser:
    """
    Parses UI agent (RL) logs from JSONL or JSON files.
    """

    def __init__(self, app_config):
        self.app_config = app_config

    def collect(self) -> List[Dict[str, Any]]:
        results = []
        agents_config = self.app_config.agents if hasattr(self.app_config, 'agents') else {}
        log_paths = agents_config.get("log_paths", []) if isinstance(agents_config, dict) else []
        root = Path(self.app_config.root_path)

        for rel_path in log_paths:
            log_dir = root / rel_path
            if not log_dir.exists():
                continue

            # Find all log files (JSONL and JSON)
            for log_file in log_dir.rglob("*"):
                if log_file.suffix in [".jsonl", ".json"] and log_file.is_file():
                    parsed = self._parse_log_file(log_file)
                    if parsed:
                        results.extend(parsed)

        return results

    def _parse_log_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse a single log file."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return []

        if file_path.suffix == ".jsonl":
            return self._parse_jsonl(content, file_path)
        elif file_path.suffix == ".json":
            return self._parse_json(content, file_path)

        return []

    def _parse_jsonl(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Parse JSONL format (one JSON object per line)."""
        steps = []
        for line in content.strip().split("\n"):
            if not line.strip():
                continue
            try:
                step = json.loads(line)
                steps.append(step)
            except json.JSONDecodeError:
                continue

        if not steps:
            return []

        return [self._create_episode_from_steps(steps, file_path)]

    def _parse_json(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Parse JSON format (array of steps)."""
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return []

        if isinstance(data, list):
            return [self._create_episode_from_steps(data, file_path)]
        elif isinstance(data, dict) and "steps" in data:
            return [self._create_episode_from_steps(data["steps"], file_path)]

        return []

    def _create_episode_from_steps(self, steps: List[Dict], file_path: Path) -> Dict[str, Any]:
        """Create an episode summary from a list of steps."""
        total_steps = len(steps)

        # Count successes and errors
        success_count = 0
        error_count = 0
        backtracks = 0

        # Extract DOM sizes
        dom_sizes = []
        urls_visited = set()
        actions = []

        for step in steps:
            # Handle different status field names
            status = step.get("status", step.get("result", "ok"))
            if status in ["ok", "passed", "success"]:
                success_count += 1
            elif status in ["error", "failed", "failure"]:
                error_count += 1
                backtracks += 1  # Assume errors lead to backtracks

            # Extract DOM length
            dom_len = step.get("dom_length", 0)
            if dom_len:
                dom_sizes.append(dom_len)

            # Extract URL
            url = step.get("url", "")
            if url:
                urls_visited.add(url)

            # Extract action info
            action = step.get("action", {})
            if isinstance(action, dict):
                action_type = action.get("strategy", action.get("type", "unknown"))
            else:
                action_type = step.get("action", "unknown")
            actions.append({"action": action_type, "selector": action.get("selector") if isinstance(action, dict) else None})

        # Determine overall success
        success = error_count == 0 or success_count > error_count

        return {
            "episode_id": file_path.stem,
            "task_id": file_path.stem,
            "success": success,
            "steps": actions,
            "steps_count": total_steps,
            "success_count": success_count,
            "error_count": error_count,
            "backtracks": backtracks,
            "unique_urls": len(urls_visited),
            "avg_dom_size": sum(dom_sizes) / len(dom_sizes) if dom_sizes else 0,
            "max_dom_size": max(dom_sizes) if dom_sizes else 0,
            "min_dom_size": min(dom_sizes) if dom_sizes else 0,
        }
