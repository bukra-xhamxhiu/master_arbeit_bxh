# web_complexity_lab/features/test_metrics.py
from typing import List, Dict, Any


def compute_test_metrics(app_id: str, tests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for t in tests:
        steps = t.get("steps", [])
        steps_count = t.get("steps_count", len(steps))

        m = {
            "app_id": app_id,
            "test_id": t.get("test_id", "unknown"),
            "file": t.get("file", ""),
            "framework": t.get("framework", "playwright"),
            "steps_count": steps_count,
            "clicks": t.get("clicks", 0),
            "fills": t.get("fills", 0),
            "navigations": t.get("navigations", 0),
            "assertions": t.get("assertions", 0),
        }
        results.append(m)
    return results
