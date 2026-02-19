from playwright.sync_api import sync_playwright
from typing import Dict, Any, Tuple


class CoffeePlaywrightEnv:
    """
    A minimal environment for controlling the Coffee Shop Website using Playwright.
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
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        self.step_count = 0
        self.visited_urls = set()
        self.trace = []
        return self._get_state()

    def _get_state(self) -> Dict[str, Any]:
        return {
            "url": self.page.url,
            "dom": self.page.content()
        }

    def step(self, action: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, Dict]:
        self.step_count += 1
        reward = 0.0
        info = {}

        before_url = self.page.url
        before_dom = self.page.content()

        try:
            if action["type"] == "click":
                self.page.click(action["selector"], timeout=2000)
            elif action["type"] == "type":
                self.page.fill(action["selector"], action["text"])
            elif action["type"] == "scroll":
                self.page.mouse.wheel(0, action["amount"])
            elif action["type"] == "goto":
                self.page.goto(action["url"], wait_until="domcontentloaded")
        except Exception as e:
            reward -= 1.0
            info["error"] = str(e)
            done = self.step_count >= self.max_steps
            next_state = self._get_state()
            self.trace.append({
                "action": action,
                "before_url": before_url,
                "after_url": next_state["url"],
                "reward": reward,
                "info": info
            })
            return next_state, reward, done, info

        after_url = self.page.url
        after_dom = self.page.content()

        # Reward logic of the agents 
        if after_url != before_url:
            reward += 1.0

        if abs(len(after_dom) - len(before_dom)) > 500:
            reward += 1.0

        if after_url not in self.visited_urls:
            reward += 2.0
            self.visited_urls.add(after_url)

        reward -= 0.05  # step penalty

        next_state = {"url": after_url, "dom": after_dom}
        done = self.step_count >= self.max_steps

        self.trace.append({
            "action": action,
            "before_url": before_url,
            "after_url": after_url,
            "reward": reward,
            "info": info
        })

        return next_state, reward, done, info

    def close(self):
        self.browser.close()
        self.playwright.stop()
