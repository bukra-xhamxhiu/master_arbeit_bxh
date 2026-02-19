# web_complexity_lab/features/test_metrics.py
from typing import List, Dict, Any
import math


def compute_test_metrics(app_id: str, tests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for t in tests:
        steps = t.get("steps", [])
        pages_visited = {s.get("url") for s in steps if "url" in s}
        actions = [s["type"] for s in steps if "type" in s]

        clicks = sum(1 for a in actions if a == "click")
        fills = sum(1 for a in actions if a == "fill")
        selects = sum(1 for a in actions if a == "select")
        scrolls = sum(1 for a in actions if a == "scroll")

        m = {
            "app_id": app_id,
            "test_id": t["test_id"],
            "steps_count": len(steps),
            "unique_pages": len(pages_visited),
            "clicks": clicks,
            "text_inputs": fills,
            "selects": selects,
            "scrolls": scrolls,
            # TODO: selector complexity, branching, loops, assertions_count, etc.
        }
        results.append(m)
    return results
