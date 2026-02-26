# web_complexity_lab/collectors/ui_structure_collector.py
from typing import List, Dict, Any
from pathlib import Path
import json
import re


class UIStructureCollector:
    """
    Collects UI structure metrics from agent logs or HTML files.
    Extracts DOM node counts, URLs visited, and page information.
    """

    def __init__(self, app_config):
        self.app_config = app_config

    def collect(self) -> List[Dict[str, Any]]:
        results = []
        root = Path(self.app_config.root_path)

        # First try to get UI data from agent logs (they have DOM info)
        agent_data = self._collect_from_agent_logs(root)
        if agent_data:
            results.extend(agent_data)

        # Also scan for HTML files if this is a static site
        html_data = self._collect_from_html_files(root)
        if html_data:
            results.extend(html_data)

        # If no data found, create a basic entry
        if not results:
            results.append({
                "page_id": "main",
                "url": self.app_config.base_url,
                "dom_node_count": 0,
                "interactive_elements": [],
                "forms": [],
            })

        return results

    def _collect_from_agent_logs(self, root: Path) -> List[Dict[str, Any]]:
        """Extract UI structure data from agent exploration logs."""
        results = []
        agents_config = self.app_config.agents if hasattr(self.app_config, 'agents') else {}
        log_paths = agents_config.get("log_paths", []) if isinstance(agents_config, dict) else []

        pages_seen = {}  # url -> {dom_sizes: [], ...}

        for rel_path in log_paths:
            log_dir = root / rel_path
            if not log_dir.exists():
                continue

            for log_file in log_dir.rglob("*"):
                if log_file.suffix not in [".jsonl", ".json"]:
                    continue

                try:
                    content = log_file.read_text(encoding="utf-8")
                    steps = self._parse_log_content(content, log_file.suffix)

                    for step in steps:
                        url = step.get("url", "")
                        dom_len = step.get("dom_length", 0)

                        if url and dom_len:
                            if url not in pages_seen:
                                pages_seen[url] = {"dom_sizes": [], "actions": []}
                            pages_seen[url]["dom_sizes"].append(dom_len)

                            # Track interactive elements from actions
                            action = step.get("action", {})
                            if isinstance(action, dict):
                                selector = action.get("selector", action.get("description", ""))
                            else:
                                selector = step.get("selector", "")
                            if selector:
                                pages_seen[url]["actions"].append(selector)

                except Exception:
                    continue

        # Convert to results format
        for url, data in pages_seen.items():
            dom_sizes = data["dom_sizes"]
            page_id = self._url_to_page_id(url)

            results.append({
                "page_id": page_id,
                "url": url,
                "dom_node_count": int(sum(dom_sizes) / len(dom_sizes)) if dom_sizes else 0,
                "max_dom_count": max(dom_sizes) if dom_sizes else 0,
                "min_dom_count": min(dom_sizes) if dom_sizes else 0,
                "interactive_elements": list(set(data["actions"])),
                "forms": [],  # Would need HTML parsing to detect forms
            })

        return results

    def _collect_from_html_files(self, root: Path) -> List[Dict[str, Any]]:
        """Scan HTML files for basic structure info."""
        results = []

        # Look for HTML files in common locations
        html_dirs = ["dist", "public", "src", "."]

        for dir_name in html_dirs:
            html_dir = root / dir_name
            if not html_dir.exists():
                continue

            for html_file in html_dir.glob("*.html"):
                try:
                    content = html_file.read_text(encoding="utf-8")
                    page_data = self._analyze_html(content, html_file)
                    if page_data:
                        results.append(page_data)
                except Exception:
                    continue

        return results

    def _analyze_html(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Basic HTML analysis without full parsing."""
        # Count various elements using regex (simple approximation)
        tags = re.findall(r"<(\w+)", content)
        dom_count = len(tags)

        # Count interactive elements
        buttons = len(re.findall(r"<button", content, re.I))
        inputs = len(re.findall(r"<input", content, re.I))
        links = len(re.findall(r"<a\s", content, re.I))
        selects = len(re.findall(r"<select", content, re.I))

        interactive_count = buttons + inputs + links + selects

        # Count forms
        forms = len(re.findall(r"<form", content, re.I))

        return {
            "page_id": file_path.stem,
            "url": f"{self.app_config.base_url}/{file_path.name}",
            "dom_node_count": dom_count,
            "interactive_elements": list(range(interactive_count)),  # Placeholder list
            "interactive_count": interactive_count,
            "buttons": buttons,
            "inputs": inputs,
            "links": links,
            "forms": list(range(forms)),
        }

    def _parse_log_content(self, content: str, suffix: str) -> List[Dict]:
        """Parse log file content based on format."""
        if suffix == ".jsonl":
            steps = []
            for line in content.strip().split("\n"):
                if line.strip():
                    try:
                        steps.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            return steps
        elif suffix == ".json":
            try:
                data = json.loads(content)
                return data if isinstance(data, list) else []
            except json.JSONDecodeError:
                return []
        return []

    def _url_to_page_id(self, url: str) -> str:
        """Convert URL to a page identifier."""
        # Extract path from URL
        if "://" in url:
            path = url.split("://", 1)[1]
            if "/" in path:
                path = path.split("/", 1)[1]
            else:
                path = ""
        else:
            path = url

        # Clean up the path
        path = path.strip("/").replace("/", "_").replace(".html", "")
        return path if path else "home"
