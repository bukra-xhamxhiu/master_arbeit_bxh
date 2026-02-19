# env/movies_env.py
#playwright environment for movies app, playwright wrapper.
from playwright.sync_api import sync_playwright
from typing import Dict, Any, Tuple, List


class MoviesPlaywrightEnv:
    """
    Environment for the Movies App.
    Handles navigation, actions, DOM capturing, rewards, and trace recording.
    """

#launches Chromium, navigates to the base URL, and provides methods to reset the environment, perform actions, and close the browser.
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
        self.trace: List[Dict[str, Any]] = []

#reset the environment to the initial state by clearing cookies, local storage, and session storage, then navigating to the base URL. It also resets the step count, visited URLs, and trace log.
    def reset(self) -> Dict[str, Any]:
        """Open the base URL fresh and clear state."""
        self.context.clear_cookies()
        self.context.set_default_timeout(5000)

        # Clear local/session storage so routing is deterministic
        self.page.add_init_script("localStorage.clear(); sessionStorage.clear();")

        self.page.goto(self.base_url, wait_until="domcontentloaded")
        self.step_count = 0
        self.visited_urls = set()
        self.trace = []

        state = self._get_state()
        print(f"Initial URL: {state['url']}\n")
        return state


#_get_state captures the current URL and DOM content of the page, returning them as a dictionary. 
# This method is used to represent the state of the environment after each action.
    def _get_state(self) -> Dict[str, Any]:
        return {
            "url": self.page.url,
            "dom": self.page.content(),
        }


#step executes a given action (click, scroll, or goto) and calculates a reward based on the resulting state. 
# It also logs the action, the before and after URLs, the reward, and any additional info (like errors) into a trace for later analysis. 
# The method returns the next state, the reward, whether the episode is done, and any other found info.
    def step(self, action: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        """
        Execute a UI action and return:
        (next_state, reward, done, info)

        Supported action types:
          - "click":  selector
          - "scroll": amount
          - "goto":   url

        Extra keys like "group" or "label" are kept and logged but ignored
        by the environment itself.
        """
        self.step_count += 1
        reward = 0.0
        info: Dict[str, Any] = {}

        before_url = self.page.url
        before_dom = self.page.content()

        # --------- Execute action ---------
        try:
            action_type = action.get("type")

            if action_type == "click":
                self.page.click(action["selector"], timeout=5000)
            elif action_type == "scroll":
                self.page.mouse.wheel(0, action["amount"])
            elif action_type == "goto":
                self.page.goto(action["url"], wait_until="domcontentloaded")
            else:
                info["error"] = f"Unknown action type: {action_type}"
                reward -= 1.0

        except Exception as e:
            reward -= 1.0
            info["error"] = str(e)

            done = self.step_count >= self.max_steps
            next_state = self._get_state()

            # Log failed step
            self.trace.append({
                "action": action,
                "before_url": before_url,
                "after_url": next_state["url"],
                "reward": reward,
                "info": info,
            })
            return next_state, reward, done, info

        # --------- Reward on success ---------
        after_url = self.page.url
        after_dom = self.page.content()

        # Reward for URL change, significant DOM change, and visiting new URLs
        if after_url != before_url:
            reward += 1.0

        if abs(len(after_dom) - len(before_dom)) > 500:
            reward += 1.0

        if after_url not in self.visited_urls:
            reward += 2.0
            self.visited_urls.add(after_url)

        # Small step penalty
        reward -= 0.05

        done = self.step_count >= self.max_steps
        next_state = {"url": after_url, "dom": after_dom}

        # Log successful step
        self.trace.append({
            "action": action,
            "before_url": before_url,
            "after_url": after_url,
            "reward": reward,
            "info": info,
        })

        return next_state, reward, done, info

    def close(self) -> None:
        self.browser.close()
        self.playwright.stop()
