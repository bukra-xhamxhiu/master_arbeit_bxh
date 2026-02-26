# web_complexity_lab/features/log_metrics.py
from typing import List, Dict, Any


def compute_log_metrics(app_id: str, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes metrics from test execution logs (JUnit, traces, etc.).
    """
    results = []
    for log in logs:
        steps = log.get("steps", [])
        total_duration = log.get("duration_ms", 0)

        passed_steps = sum(1 for s in steps if s.get("status") == "passed")
        failed_steps = sum(1 for s in steps if s.get("status") == "failed")

        m = {
            "app_id": app_id,
            "test_id": log.get("test_id"),
            "status": log.get("status"),
            "duration_ms": total_duration,
            "steps_count": len(steps),
            "passed_steps": passed_steps,
            "failed_steps": failed_steps,
            "retries": log.get("retries", 0),
            "failure_count": len(log.get("failures", [])),
        }
        results.append(m)
    return results
