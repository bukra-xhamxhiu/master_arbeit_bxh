# web_complexity_lab/features/aggregation.py
from typing import List, Dict, Any
import statistics as stats


def _safe_mean(values):
    return stats.mean(values) if values else 0.0


def aggregate_per_app(
    app_id: str,
    ui_metrics: List[Dict[str, Any]],
    test_metrics: List[Dict[str, Any]],
    log_metrics: List[Dict[str, Any]],
    agent_metrics: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Aggregates per-app stats that feed into complexity indices.
    """
    dom_counts = [m["dom_node_count"] for m in ui_metrics]
    steps_counts = [m["steps_count"] for m in test_metrics]
    test_durations = [m["duration_ms"] for m in log_metrics if "duration_ms" in m]
    agent_steps = [m["steps_to_success"] for m in agent_metrics if "steps_to_success" in m]

    return {
        "app_id": app_id,
        "avg_dom_nodes": _safe_mean(dom_counts),
        "max_dom_nodes": max(dom_counts) if dom_counts else 0,
        "avg_test_steps": _safe_mean(steps_counts),
        "avg_test_duration_ms": _safe_mean(test_durations),
        "avg_agent_steps_to_success": _safe_mean(agent_steps),
        # TODO: add flakiness rate, error diversity, backtracks, etc.
    }
