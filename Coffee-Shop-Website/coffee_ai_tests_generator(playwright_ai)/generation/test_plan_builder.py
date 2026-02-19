class TestPlanBuilder:
    """
    Converts an exploration trace into a structured test plan.
    Only keeps successful click actions.
    """

    def build_test_plan(self, trace):
        steps = []

        for entry in trace:
            action = entry["action"]
            info = entry["info"]

            # ignore failed clicks
            if "error" in info:
                continue

            if action["type"] == "click":
                steps.append({
                    "action": "click",
                    "selector": action["selector"]
                })

        return steps
