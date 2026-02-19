# web_complexity_lab/features/ui_metrics.py
from typing import List, Dict, Any
import statistics as stats


def compute_ui_metrics(app_id: str, ui_states: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes per-page / per-state UI metrics.
    """
    metrics = []
    for state in ui_states:
        interactive_elems = state.get("interactive_elements", [])
        forms = state.get("forms", [])

        m = {
            "app_id": app_id,
            "page_id": state.get("page_id"),
            "url": state.get("url"),
            "dom_node_count": state.get("dom_node_count", 0),
            "interactive_count": len(interactive_elems),
            "form_count": len(forms),
            # TODO: menu_depth, layout_density, etc.
        }
        metrics.append(m)
    return metrics
