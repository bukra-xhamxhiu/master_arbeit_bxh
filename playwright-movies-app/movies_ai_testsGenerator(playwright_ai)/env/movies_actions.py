from typing import List, Dict


def get_clickable_elements(page) -> List[Dict[str, str]]:
    """
    Extract a variety of clickable elements in the Movies App:
    - Header/nav links & buttons
    - Movie cards
    - Generic buttons with text
    """

    elements: List[Dict[str, str]] = []

    def add_textual_elements(selector: str):
        loc = page.locator(selector)
        count = loc.count()
        for i in range(count):
            e = loc.nth(i)
            text = e.inner_text().strip()
            if not text:
                continue
            elements.append({
                "selector": f"{selector}:has-text('{text}')",
                "text": text,
            })

    # Header / nav items
    add_textual_elements("header a")
    add_textual_elements("header button")
    add_textual_elements("nav a")
    add_textual_elements("nav button")

    # Generic buttons with text anywhere
    add_textual_elements("button")

    # Movie cards (data-testid or class-based)
    cards = page.locator("[data-testid='movie-card'], .movie-card")
    count_cards = cards.count()
    for i in range(count_cards):
        elements.append({
            "selector": f"[data-testid='movie-card'] >> nth={i}",
            "text": "movie-card",
        })

    return elements


def create_click_action(selector: str) -> Dict[str, str]:
    return {"type": "click", "selector": selector}
