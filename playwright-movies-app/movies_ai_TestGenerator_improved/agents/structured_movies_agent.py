# agents/structured_movies_agent.py
from typing import List, Dict, Any

from env.movies_env import MoviesPlaywrightEnv
from env.movies_actions import (
    get_menu_items,
    get_movie_cards,
    get_theme_toggle_selector,
    create_click_action,
)


class StructuredMoviesAgent:
    """
    Agent that explores:
      - Menus (header/nav)
      - Navigation paths (movie cards)
      - Actions on detail pages (scroll + theme toggle)
    """

    def __init__(self, env: MoviesPlaywrightEnv, max_steps: int = 40):
        self.env = env
        self.max_steps = max_steps

    def run(self) -> List[Dict[str, Any]]:
        """
        Run structured exploration and return the environment trace.
        """
        self.env.reset()

        self._explore_menus()
        self._explore_cards_with_actions(max_cards=3)

        return self.env.trace

    # ---------------- MENUS ----------------
    def _explore_menus(self) -> None:
        print("=== MENU EXPLORATION ===")
        page = self.env.page
        items = get_menu_items(page)

        if not items:
            print("  [Menu] No menu items detected.")
            return

        for item in items:
            text = item["text"]
            selector = item["selector"]
            print(f"  [Menu] Click '{text}' with selector {selector}")

            action = create_click_action(selector, group="menus")
            next_state, reward, done, info = self.env.step(action)

            if done or self.env.step_count >= self.max_steps:
                return

            # Go back to base page after each menu click
            self.env.page.goto(self.env.base_url, wait_until="domcontentloaded")

    # ------------- NAVIGATION + ACTIONS -------------
    def _explore_cards_with_actions(self, max_cards: int = 3) -> None:
        print("\n=== NAVIGATION & ACTIONS EXPLORATION ===")

        # Ensure we're on the base page with the cards visible
        self.env.page.goto(self.env.base_url, wait_until="domcontentloaded")
        page = self.env.page

        cards = get_movie_cards(page, max_cards=max_cards)
        if not cards:
            print("  [Cards] No movie cards detected on base page.")
            return

        for idx, card in enumerate(cards):
            label = card["text"] or f"card_{idx}"
            selector = card["selector"]
            print(f"  [Card] Click card {idx} ({label}) with selector {selector}")

            nav_action = create_click_action(selector, group="navigation")
            next_state, reward, done, info = self.env.step(nav_action)

            if done or self.env.step_count >= self.max_steps:
                return

            # Actions on detail page
            self._actions_on_current_page()

            if self.env.step_count >= self.max_steps:
                return

            # Go back to base page for next card
            self.env.page.goto(self.env.base_url, wait_until="domcontentloaded")

    def _actions_on_current_page(self) -> None:
        """
        On the current page, perform:
          - scroll
          - theme toggle if available
        """
        print("    [Actions] Scroll and attempt theme toggle")

        # Scroll down
        scroll_action = {"type": "scroll", "amount": 1000, "group": "actions"}
        self.env.step(scroll_action)

        # Theme toggle
        selector = get_theme_toggle_selector(self.env.page)
        if selector:
            print(f"    [Actions] Toggle theme via {selector}")
            toggle_action = create_click_action(selector, group="actions")
            self.env.step(toggle_action)
