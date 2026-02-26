# web_complexity_lab/features/aggregation.py
from typing import List, Dict, Any
import statistics as stats


def _safe_mean(values):
    return stats.mean(values) if values else 0.0


def _safe_max(values):
    return max(values) if values else 0


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
    # UI metrics aggregation
    dom_counts = [m["dom_node_count"] for m in ui_metrics if m.get("dom_node_count")]
    interactive_counts = [m.get("interactive_count", 0) for m in ui_metrics]
    form_counts = [m.get("form_count", 0) for m in ui_metrics]

    # Test metrics aggregation
    steps_counts = [m["steps_count"] for m in test_metrics if m.get("steps_count")]
    clicks = [m.get("clicks", 0) for m in test_metrics]
    assertions = [m.get("assertions", 0) for m in test_metrics]

    # Log metrics aggregation
    test_durations = [m["duration_ms"] for m in log_metrics if m.get("duration_ms")]
    failure_count = sum(1 for m in log_metrics if m.get("status") == "failed")
    total_logs = len(log_metrics) if log_metrics else 1

    # Agent metrics aggregation
    agent_steps = [m["steps_count"] for m in agent_metrics if m.get("steps_count")]
    agent_success = [1 for m in agent_metrics if m.get("success")]
    agent_backtracks = [m.get("backtracks", 0) for m in agent_metrics]
    agent_dom_sizes = [m.get("avg_dom_size", 0) for m in agent_metrics if m.get("avg_dom_size")]

    return {
        "app_id": app_id,
        # UI metrics
        "total_pages": len(ui_metrics),
        "avg_dom_nodes": _safe_mean(dom_counts),
        "max_dom_nodes": _safe_max(dom_counts),
        "avg_interactive_count": _safe_mean(interactive_counts),
        "avg_form_count": _safe_mean(form_counts),
        # Test metrics
        "total_tests": len(test_metrics),
        "avg_test_steps": _safe_mean(steps_counts),
        "total_clicks": sum(clicks),
        "total_assertions": sum(assertions),
        # Log metrics
        "avg_test_duration_ms": _safe_mean(test_durations),
        "failure_rate": failure_count / total_logs,
        # Agent metrics
        "total_episodes": len(agent_metrics),
        "avg_agent_steps_to_success": _safe_mean(agent_steps),
        "agent_success_rate": len(agent_success) / len(agent_metrics) if agent_metrics else 0,
        "avg_agent_backtracks": _safe_mean(agent_backtracks),
        "avg_agent_dom_size": _safe_mean(agent_dom_sizes),
    }
