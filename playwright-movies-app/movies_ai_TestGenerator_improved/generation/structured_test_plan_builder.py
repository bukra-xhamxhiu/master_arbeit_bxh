# generation/structured_test_plan_builder.py
from typing import List, Dict, Any
from collections import defaultdict


class StructuredTestPlanBuilder:
    """
    Build grouped test plans from the environment trace.

    Output:
      {
        "menus":      [ {type, selector}, ... ],
        "navigation": [ {type, selector}, ... ],
        "actions":    [ {type, selector} or {type, amount}, ... ],
      }
    """

    def build(self, trace: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

        for entry in trace:
            action = entry.get("action", {}) or {}
            info = entry.get("info", {}) or {}

            # Skip failed actions
            if info.get("error"):
                continue

            action_type = action.get("type")
            if action_type not in ("click", "scroll"):
                continue

            group = action.get("group") or "navigation"

            step: Dict[str, Any] = {"type": action_type, "group": group}

            if action_type == "click":
                selector = action.get("selector")
                if not selector:
                    continue
                step["selector"] = selector

            if action_type == "scroll":
                step["amount"] = action.get("amount", 0)

            groups[group].append(step)

        return dict(groups)
