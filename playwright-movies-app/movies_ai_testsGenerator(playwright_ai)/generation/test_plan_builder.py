# generation/test_plan_builder.py

class TestPlanBuilder:
    """
    Builds a test plan (sequence of UI steps) from an environment trace.

    Supported action types from env.trace["action"]["type"]:
      - "click"            with "selector"
      - "click_by_label"   with "label"
      - "click_by_role"    with "role" + "name"

    Filtering logic:
      - Keep only successful actions (no info["error"])
      - Skip overly generic selectors ("a", "button")
      - Skip auth-related actions (Login/Logout/Sign in/Sign out)
      - Skip consecutive duplicates
    """

    AUTH_KEYWORDS = (
        "login",
        "log in",
        "logout",
        "log out",
        "sign in",
        "sign out",
        "auth",
        "access",
    )

    def _contains_auth_keyword(self, text: str | None) -> bool:
        if not text:
            return False
        s = text.lower()
        return any(k in s for k in self.AUTH_KEYWORDS)

    def build_test_plan(self, trace):
        steps = []
        last_signature = None

        for entry in trace:
            action = entry.get("action", {}) or {}
            info = entry.get("info", {}) or {}

            # Skip failed actions
            if "error" in info and info["error"]:
                continue

            a_type = action.get("type")

            # ---------------------------
            # 1) selector-based clicks
            # ---------------------------
            if a_type == "click":
                selector = action.get("selector")
                if not selector:
                    continue

                # skip generic, useless selectors
                if selector in ("a", "button"):
                    continue

                # simple auth filter on selector text
                if self._contains_auth_keyword(selector):
                    continue

                step = {
                    "action": "click",
                    "selector": selector,
                }

            # ---------------------------
            # 2) click_by_label
            # ---------------------------
            elif a_type == "click_by_label":
                label = action.get("label")
                if not label:
                    continue

                # auth filter
                if self._contains_auth_keyword(label):
                    continue

                step = {
                    "action": "click_by_label",
                    "label": label,
                }

            # ---------------------------
            # 3) click_by_role
            # ---------------------------
            elif a_type == "click_by_role":
                role = action.get("role")
                name = action.get("name")
                if not role or not name:
                    continue

                # auth filter by accessible name
                if self._contains_auth_keyword(name):
                    continue

                step = {
                    "action": "click_by_role",
                    "role": role,
                    "name": name,
                }

            else:
                # ignore other types (fill, scroll, press_key, etc.)
                continue

            # Deduplicate consecutive identical steps
            signature = tuple(sorted(step.items()))
            if signature == last_signature:
                continue

            steps.append(step)
            last_signature = signature

        return steps
