from playwright.sync_api import sync_playwright
from typing import Dict, Any, Tuple

# ---------------------------------------------------------------------
# LOGIN SNAPSHOT
# ---------------------------------------------------------------------

#
# WARNING: – do NOT commit  to GitHub.
#
LOGIN_INIT_SCRIPT = """
// Preload a logged-in session into localStorage

// Email (only if you actually have a key for it)
window.localStorage.setItem('email', 'bukra@gmail.com');

// JWT token
window.localStorage.setItem(
  'token',
  'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MjMsInVzZXJuYW1lIjoiaGVsbG8iLCJlbWFpbCI6ImJ1a3JhQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiZjU2ODdkZTRhNjc4MzhlZDQwNTZmMmNmMDdmNzFjNDQiLCJyb2xlIjoiY3VzdG9tZXIiLCJkZWx1eGVUb2tlbiI6IiIsImxhc3RMb2dpbklwIjoiMC4wLjAuMCIsInByb2ZpbGVJbWFnZSI6Ii9hc3NldHMvcHVibGljL2ltYWdlcy91cGxvYWRzL2RlZmF1bHQuc3ZnIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDI1LTEwLTA2VDIzOjE1OjM2LjkxN1oiLCJ1cGRhdGVkQXQiOiIyMDI1LTEwLTA2VDIzOjIyOjI5LjIxM1oiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE3NTk3OTI5NDl9.dN-aRON6muyDxI1YLPRJNkW9AhzqghxdlFxmwn1v04-espHcVqsPl0FQFbsvOfwbRR_pVDbrdoTKy4CJUji1qwIAegZFa6fOCP78u0RS59M3EUsiqcJPRZffF8K10plUpb85LDU1tWUTuBz3TIK0yeZUlKXkkAywF7NrZjtzgEs'
);

// Auth object from key `zaps.movies.dev`
window.localStorage.setItem(
  'zaps.movies.dev',
  '{"request_token":"","access_token":"{"request_token":"","access_token":"eyJhY2NvdW50X2lkIjoidnZ2JTQwZ21haWwuY29tIn0=","account_id":"vvv%40gmail.com"}"}'
);
"""


class MoviesPlaywrightEnv:
    """
    Environment for the Movies App.

    reset() always starts from a logged-in state by injecting localStorage
    before the first navigation.
    """

    def __init__(self, base_url: str, headless: bool = True, max_steps: int = 50):
        self.base_url = base_url
        self.headless = headless
        self.max_steps = max_steps

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

        self.step_count = 0
        self.visited_urls = set()
        self.trace = []

    def reset(self) -> Dict[str, Any]:
        """
        Open the base URL in a clean but already-authenticated state.
        """

        # Clear cookies etc.
        self.context.clear_cookies()
        self.context.set_default_timeout(8000)

        # Important: clear old storage and inject our login snapshot
        self.page.add_init_script("localStorage.clear(); sessionStorage.clear();")
        self.page.add_init_script(LOGIN_INIT_SCRIPT)

        # Now go to the app; it should see us as logged in
        self.page.goto(self.base_url, wait_until="domcontentloaded")

        self.step_count = 0
        self.visited_urls = set()
        self.trace = []

        return self._get_state()

    def _get_state(self) -> Dict[str, Any]:
        return {
            "url": self.page.url,
            "dom": self.page.content(),
        }

    def step(self, action: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, Dict]:
        """
        Execute a UI action and return:
        (next_state, reward, done, info)
        """
        self.step_count += 1
        reward = 0.0
        info: Dict[str, Any] = {}

        before_url = self.page.url
        before_dom = self.page.content()

        try:
            action_type = action.get("type")

            if action_type == "click":
                self.page.click(action["selector"], timeout=5000)

            elif action_type == "type":
                self.page.fill(action["selector"], action["text"])

            elif action_type == "scroll":
                self.page.mouse.wheel(0, action["amount"])

            elif action_type == "goto":
                self.page.goto(action["url"], wait_until="domcontentloaded")

            elif action_type == "click_by_label":
                self.page.get_by_label(action["label"]).click(timeout=5000)

            elif action_type == "fill_by_label":
                self.page.get_by_label(action["label"]).fill(action["text"])

            elif action_type == "click_by_role":
                self.page.get_by_role(
                    action["role"], name=action["name"]
                ).click(timeout=5000)

            elif action_type == "fill_by_placeholder":
                self.page.get_by_placeholder(action["placeholder"]).fill(
                    action["text"]
                )

            elif action_type == "press_key":
                self.page.keyboard.press(action["key"])

            else:
                info["error"] = f"Unknown action type: {action_type}"
                reward -= 1.0

        except Exception as e:
            reward -= 1.0
            info["error"] = str(e)

            done = self.step_count >= self.max_steps
            next_state = self._get_state()

            self.trace.append(
                {
                    "action": action,
                    "before_url": before_url,
                    "after_url": next_state["url"],
                    "reward": reward,
                    "info": info,
                }
            )
            return next_state, reward, done, info

        after_url = self.page.url
        after_dom = self.page.content()

        if after_url != before_url:
            reward += 1.0

        if abs(len(after_dom) - len(before_dom)) > 500:
            reward += 1.0

        if after_url not in self.visited_urls:
            reward += 2.0
            self.visited_urls.add(after_url)

        reward -= 0.05

        next_state = {"url": after_url, "dom": after_dom}
        done = self.step_count >= self.max_steps

        self.trace.append(
            {
                "action": action,
                "before_url": before_url,
                "after_url": after_url,
                "reward": reward,
                "info": info,
            }
        )

        return next_state, reward, done, info

    def close(self) -> None:
        self.browser.close()
        self.playwright.stop()
