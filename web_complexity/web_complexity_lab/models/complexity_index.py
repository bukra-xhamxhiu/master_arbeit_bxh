# web_complexity_lab/models/complexity_index.py
from typing import Dict, Any

def _normalize(value: float, min_v: float, max_v: float) -> float:
    """
    Linearly normalize value into [0, 1] given an expected range [min_v, max_v].
    Values below min_v are clipped to 0, above max_v to 1.
    """
    if max_v <= min_v:
        return 0.0
    x = (value - min_v) / (max_v - min_v)
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _safe_get(app_level: Dict[str, Any], key: str, default: float = 0.0) -> float:
    v = app_level.get(key, default)
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def compute_suci(app_level: Dict[str, Any]) -> float:
    """
    Structural UI Complexity Index (SUCI)

    Uses mainly static UI metrics:
      - avg_dom_nodes: average DOM node count over pages
      - max_dom_nodes: maximum DOM node count
      - avg_interactive_count: average number of interactive elements
      - avg_form_count: average number of forms per page
    """

    avg_dom_nodes = _safe_get(app_level, "avg_dom_nodes")
    max_dom_nodes = _safe_get(app_level, "max_dom_nodes")
    avg_interactive = _safe_get(app_level, "avg_interactive_count")
    avg_forms = _safe_get(app_level, "avg_form_count")

    # Example expected ranges (you can tune these later based on your data)
    n_avg_dom = _normalize(avg_dom_nodes, 100, 2000)
    n_max_dom = _normalize(max_dom_nodes, 200, 4000)
    n_interactive = _normalize(avg_interactive, 5, 100)
    n_forms = _normalize(avg_forms, 0, 10)

    # Simple average of the available components
    components = [n_avg_dom, n_max_dom, n_interactive, n_forms]
    components = [c for c in components if c is not None]
    if not components:
        return 0.0
    return sum(components) / len(components)


def compute_ifci(app_level: Dict[str, Any]) -> float:
    """
    Interaction Flow Complexity Index (IFCI)

    Uses interaction and test-structure metrics:
      - avg_test_steps: median/average steps per test
      - avg_unique_pages: average number of distinct pages per test
      - avg_action_diversity: distinct action types per test
    """

    avg_steps = _safe_get(app_level, "avg_test_steps")
    avg_pages = _safe_get(app_level, "avg_unique_pages")
    avg_action_div = _safe_get(app_level, "avg_action_diversity")

    n_steps = _normalize(avg_steps, 3, 40)
    n_pages = _normalize(avg_pages, 1, 10)
    n_action_div = _normalize(avg_action_div, 1, 8)

    components = [n_steps, n_pages, n_action_div]
    components = [c for c in components if c is not None]
    if not components:
        return 0.0
    return sum(components) / len(components)


def compute_trci(app_level: Dict[str, Any]) -> float:
    """
    Temporal /  Complexity Index (TRCI)

    Uses execution-log metrics:
      - avg_test_duration_ms: average test duration
      - failure_rate: proportion of failed tests (0..1)
      - flakiness_rate: proportion of flaky tests (0..1)
    """

    avg_duration_ms = _safe_get(app_level, "avg_test_duration_ms")
    failure_rate = _safe_get(app_level, "failure_rate")
    flakiness_rate = _safe_get(app_level, "flakiness_rate")

    # Assume typical tests range from 0.5s to 20s
    n_dur = _normalize(avg_duration_ms, 500, 20000)
    # failure_rate and flakiness_rate are already in 0..1, just clip
    n_fail = _normalize(failure_rate, 0.0, 1.0)
    n_flaky = _normalize(flakiness_rate, 0.0, 0.5)  # 50% flakiness already "max bad"

    components = [n_dur, n_fail, n_flaky]
    components = [c for c in components if c is not None]
    if not components:
        return 0.0
    return sum(components) / len(components)


def compute_adi(app_level: Dict[str, Any]) -> float:
    """
    Agent Difficulty Index (ADI)

    Uses agent metrics:
      - avg_agent_steps_to_success: average steps in successful episodes
      - agent_success_rate: fraction of successful episodes (0..1)
      - avg_agent_backtracks: average backtracks per episode
    """

    steps_to_success = _safe_get(app_level, "avg_agent_steps_to_success")
    success_rate = _safe_get(app_level, "agent_success_rate")
    backtracks = _safe_get(app_level, "avg_agent_backtracks")

    n_steps = _normalize(steps_to_success, 3, 50)
    # Low success_rate is worse, so invert: more difficulty -> higher ADI
    n_success_inverted = 1.0 - _normalize(success_rate, 0.0, 1.0)
    n_backtracks = _normalize(backtracks, 0, 15)

    components = [n_steps, n_success_inverted, n_backtracks]
    components = [c for c in components if c is not None]
    if not components:
        return 0.0
    return sum(components) / len(components)


def compute_complexity_indices(app_level: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes all indices for a single application-level metrics row.

    Required keys in app_level (used if present):
      - avg_dom_nodes, max_dom_nodes, avg_interactive_count, avg_form_count
      - avg_test_steps, avg_unique_pages, avg_action_diversity
      - avg_test_duration_ms, failure_rate, flakiness_rate
      - avg_agent_steps_to_success, agent_success_rate, avg_agent_backtracks
    """

    suci = compute_suci(app_level)
    ifci = compute_ifci(app_level)
    trci = compute_trci(app_level)
    adi = compute_adi(app_level)

    # Equal weights for now 
    w_suci = 0.25
    w_ifci = 0.25
    w_trci = 0.25
    w_adi = 0.25

    wcs = w_suci * suci + w_ifci * ifci + w_trci * trci + w_adi * adi

    return {
        "app_id": app_level["app_id"],
        "suci": suci,
        "ifci": ifci,
        "trci": trci,
        "adi": adi,
        "wcs": wcs,
    }



"""
def _normalize(value: float, min_v: float, max_v: float) -> float:
    if max_v == min_v:
        return 0.0
    return max(0.0, min(1.0, (value - min_v) / (max_v - min_v)))

def compute_complexity_indices(app_level: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes SUCI, IFCI, TRCI, ADI, and composite WCS.
    For now use simple hand-crafted normalization ranges.
    Later must be refine based on custom dataset.
    """

    suci = _normalize(app_level.get("avg_dom_nodes", 0), 100, 2000)
    ifci = _normalize(app_level.get("avg_test_steps", 0), 3, 40)
    trci = _normalize(app_level.get("avg_test_duration_ms", 0), 500, 20000)
    adi = _normalize(app_level.get("avg_agent_steps_to_success", 0), 3, 50)

    wcs = 0.25 * suci + 0.25 * ifci + 0.25 * trci + 0.25 * adi

    return {
        "app_id": app_level["app_id"],
        "suci": suci,
        "ifci": ifci,
        "trci": trci,
        "adi": adi,
        "wcs": wcs,
    }
"""