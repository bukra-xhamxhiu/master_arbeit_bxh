# web_complexity_lab/models/complexity_index.py
from typing import Dict, Any
import math


def _normalize(value: float, min_v: float, max_v: float) -> float:
    """
    Linearly normalize value into [0, 1] given an expected range [min_v, max_v].
    """
    if max_v <= min_v:
        return 0.0
    x = (value - min_v) / (max_v - min_v)
    return max(0.0, min(1.0, x))


def _log_normalize(value: float, min_v: float, max_v: float) -> float:
    """
    Logarithmic normalization for values with large ranges.
    """
    if value <= 0:
        return 0.0
    if max_v <= min_v:
        return 0.0
    log_val = math.log1p(value)
    log_min = math.log1p(min_v)
    log_max = math.log1p(max_v)
    x = (log_val - log_min) / (log_max - log_min)
    return max(0.0, min(1.0, x))


def _safe_get(app_level: Dict[str, Any], key: str, default: float = 0.0) -> float:
    v = app_level.get(key, default)
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def compute_suci(app_level: Dict[str, Any]) -> float:
    """
    Structural UI Complexity Index (SUCI)

    Considers:
      - Number of pages/views (penalize too many simple pages)
      - DOM complexity (if available)
      - Interactive elements
      - Form count
      - Application type (SPA vs static)
    """
    total_pages = _safe_get(app_level, "total_pages")
    avg_dom_nodes = _safe_get(app_level, "avg_dom_nodes")
    avg_interactive = _safe_get(app_level, "avg_interactive_count")
    avg_forms = _safe_get(app_level, "avg_form_count")
    total_tests = _safe_get(app_level, "total_tests")

    # Cap DOM nodes at reasonable values (agent logs may have character counts)
    # Real DOM node counts are typically < 10,000
    if avg_dom_nodes > 100000:
        avg_dom_nodes = avg_dom_nodes / 100  # Likely character count, estimate nodes

    # Normalize each component
    n_pages = _normalize(total_pages, 1, 15)
    n_dom = _log_normalize(avg_dom_nodes, 100, 10000)
    n_interactive = _normalize(avg_interactive, 1, 30)
    n_forms = _normalize(avg_forms, 0, 5)

    # SPA indicator: few pages but many tests suggests complex SPA
    spa_factor = 0.0
    if total_pages <= 3 and total_tests > 5:
        spa_factor = 0.3  # Boost for SPAs

    # Many pages with few tests suggests simple static site
    static_penalty = 0.0
    if total_pages > 5 and total_tests <= 2:
        static_penalty = 0.2  # Penalty for simple multi-page static sites

    # Weight components
    components = []
    weights = []

    if total_pages > 0:
        components.append(n_pages)
        weights.append(0.25)
    if avg_dom_nodes > 0:
        components.append(n_dom)
        weights.append(0.25)
    if avg_interactive > 0:
        components.append(n_interactive)
        weights.append(0.30)
    if avg_forms > 0:
        components.append(n_forms)
        weights.append(0.20)

    if not components:
        return 0.0

    # Weighted average with adjustments
    total_weight = sum(weights)
    base_score = sum(c * w for c, w in zip(components, weights)) / total_weight

    return max(0.0, min(1.0, base_score + spa_factor - static_penalty))


def compute_ifci(app_level: Dict[str, Any]) -> float:
    """
    Interaction Flow Complexity Index (IFCI)

    Based on test complexity metrics:
      - Total number of tests (more tests = more complex app)
      - Average steps per test
      - Total interactions (clicks, assertions)
    """
    total_tests = _safe_get(app_level, "total_tests")
    avg_steps = _safe_get(app_level, "avg_test_steps")
    total_clicks = _safe_get(app_level, "total_clicks")
    total_assertions = _safe_get(app_level, "total_assertions")
    total_pages = _safe_get(app_level, "total_pages")

    # Normalize - use log scale for counts
    n_tests = _log_normalize(total_tests, 1, 200)  # 1-200 tests range
    n_steps = _normalize(avg_steps, 1, 20)
    n_clicks = _log_normalize(total_clicks, 1, 500)
    n_assertions = _log_normalize(total_assertions, 1, 1000)

    components = []
    weights = []

    if total_tests > 0:
        components.append(n_tests)
        weights.append(0.40)  # Number of tests is most important
    if avg_steps > 0:
        components.append(n_steps)
        weights.append(0.20)
    if total_clicks > 0:
        components.append(n_clicks)
        weights.append(0.20)
    if total_assertions > 0:
        components.append(n_assertions)
        weights.append(0.20)

    if not components:
        return 0.0

    total_weight = sum(weights)
    base_score = sum(c * w for c, w in zip(components, weights)) / total_weight

    # Penalize simple multi-page static sites with few tests
    # (many pages + few tests = simple navigation, not complex interactions)
    if total_pages > 5 and total_tests <= 2:
        base_score *= 0.4  # 60% penalty for static sites

    return base_score


def compute_trci(app_level: Dict[str, Any]) -> float:
    """
    Temporal / Runtime Complexity Index (TRCI)

    Based on execution metrics:
      - Test duration
      - Failure rate
    """
    avg_duration_ms = _safe_get(app_level, "avg_test_duration_ms")
    failure_rate = _safe_get(app_level, "failure_rate")

    n_dur = _normalize(avg_duration_ms, 500, 30000)
    n_fail = _normalize(failure_rate, 0.0, 0.5)

    components = []
    if avg_duration_ms > 0:
        components.append(n_dur)
    components.append(n_fail)  # Include even if 0

    if not components:
        return 0.0
    return sum(components) / len(components)


def compute_adi(app_level: Dict[str, Any]) -> float:
    """
    Agent Difficulty Index (ADI)

    Based on agent exploration metrics (if available):
      - Steps to complete tasks
      - Success rate (inverted - lower success = higher difficulty)
      - Backtracks
      - DOM complexity encountered

    If no agent data, estimate from test complexity.
    """
    total_episodes = _safe_get(app_level, "total_episodes")
    total_tests = _safe_get(app_level, "total_tests")

    if total_episodes > 0:
        # We have agent data
        steps_to_success = _safe_get(app_level, "avg_agent_steps_to_success")
        success_rate = _safe_get(app_level, "agent_success_rate")
        backtracks = _safe_get(app_level, "avg_agent_backtracks")
        avg_dom = _safe_get(app_level, "avg_agent_dom_size")

        # Cap DOM size (may be character counts)
        if avg_dom > 100000:
            avg_dom = avg_dom / 100

        n_steps = _normalize(steps_to_success, 3, 20)
        n_success_inv = 1.0 - _normalize(success_rate, 0.0, 1.0)
        n_backtracks = _normalize(backtracks, 0, 3)  # Tighter range - backtracks matter more
        n_dom = _log_normalize(avg_dom, 100, 10000)

        # Backtracks are a strong indicator of difficulty
        base_score = (n_steps * 0.25 + n_success_inv * 0.15 + n_backtracks * 0.45 + n_dom * 0.15)

        # Boost if there are also many tests (indicates complex app)
        if total_tests > 10:
            base_score += 0.1

        # Boost for any backtracks (errors encountered = harder app)
        if backtracks > 0:
            base_score += 0.15

        return min(1.0, base_score)
    else:
        # Estimate ADI from test complexity
        # More tests and more steps suggest higher agent difficulty
        avg_steps = _safe_get(app_level, "avg_test_steps")
        total_clicks = _safe_get(app_level, "total_clicks")

        n_tests = _log_normalize(total_tests, 1, 200)
        n_steps = _normalize(avg_steps, 1, 20)
        n_clicks = _log_normalize(total_clicks, 1, 500)

        components = []
        if total_tests > 0:
            components.append(n_tests * 0.85)
        if avg_steps > 0:
            components.append(n_steps * 0.85)
        if total_clicks > 0:
            components.append(n_clicks * 0.85)

        if not components:
            return 0.0
        return sum(components) / len(components)


def compute_complexity_indices(app_level: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes all complexity indices for an application.

    Indices:
      - SUCI: Structural UI Complexity Index
      - IFCI: Interaction Flow Complexity Index
      - TRCI: Temporal/Runtime Complexity Index
      - ADI: Agent Difficulty Index
      - WCS: Weighted Complexity Score (composite)
    """
    suci = compute_suci(app_level)
    ifci = compute_ifci(app_level)
    trci = compute_trci(app_level)
    adi = compute_adi(app_level)

    # Dynamic weights based on data availability and app characteristics
    total_tests = _safe_get(app_level, "total_tests")
    total_episodes = _safe_get(app_level, "total_episodes")
    backtracks = _safe_get(app_level, "avg_agent_backtracks")

    # Base weights
    w_suci = 0.20
    w_ifci = 0.30
    w_trci = 0.10
    w_adi = 0.40  # Agent difficulty is important

    # If app has many tests, IFCI is more reliable
    if total_tests > 20:
        w_ifci = 0.40
        w_adi = 0.30

    # If app has backtracks, ADI is more meaningful (harder app)
    if backtracks > 0:
        w_adi = 0.45
        w_ifci = 0.25

    # Normalize weights
    total_w = w_suci + w_ifci + w_trci + w_adi
    w_suci /= total_w
    w_ifci /= total_w
    w_trci /= total_w
    w_adi /= total_w

    wcs = w_suci * suci + w_ifci * ifci + w_trci * trci + w_adi * adi

    return {
        "app_id": app_level["app_id"],
        "suci": round(suci, 4),
        "ifci": round(ifci, 4),
        "trci": round(trci, 4),
        "adi": round(adi, 4),
        "wcs": round(wcs, 4),
    }
