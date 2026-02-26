# web_complexity_lab/features/ui_metrics.py
from typing import List, Dict, Any


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
            "interactive_count": state.get("interactive_count", len(interactive_elems)),
            "form_count": len(forms),
            "buttons": state.get("buttons", 0),
            "inputs": state.get("inputs", 0),
            "links": state.get("links", 0),
        }
        metrics.append(m)
    return metrics
