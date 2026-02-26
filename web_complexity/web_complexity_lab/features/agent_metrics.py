# web_complexity_lab/features/agent_metrics.py
from typing import List, Dict, Any


def compute_agent_metrics(app_id: str, episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes metrics from AI agent exploration logs.
    """
    results = []
    for ep in episodes:
        m = {
            "app_id": app_id,
            "episode_id": ep.get("episode_id", "unknown"),
            "task_id": ep.get("task_id", ""),
            "success": ep.get("success", False),
            "steps_count": ep.get("steps_count", 0),
            "success_count": ep.get("success_count", 0),
            "error_count": ep.get("error_count", 0),
            "backtracks": ep.get("backtracks", 0),
            "unique_urls": ep.get("unique_urls", 0),
            "avg_dom_size": ep.get("avg_dom_size", 0),
            "max_dom_size": ep.get("max_dom_size", 0),
        }
        results.append(m)
    return results
