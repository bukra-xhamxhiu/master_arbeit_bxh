from playwright.sync_api import Page
from typing import List, Dict

#will detect <a>, <button>, role = button and submits and for each element found, it created an
#action, 
def get_clickable_elements(page: Page) -> List[Dict]:
    """
    Returns a list of all clickable elements on the page.
    Each element is described by:
        { "selector": <css selector>, "text": <inner text>, "tag": <element tag> }
    """

    # CSS selectors we consider as "clickable"
    selectors = ["a", "button", "[role='button']", "input[type='submit']"]

    clickable = []

    for sel in selectors:
        try:
            elements = page.query_selector_all(sel)
        except:
            continue

        for el in elements:
            try:
                text = el.inner_text().strip()
                tag = el.evaluate("e => e.tagName.toLowerCase()")
                # Build a robust selector based on CSS + text
                selector_repr = f"{sel}:has-text('{text}')" if text else sel

                clickable.append({
                    "selector": selector_repr,
                    "text": text,
                    "tag": tag
                })
            except:
                continue

    return clickable


def create_click_action(selector: str) -> Dict:
    """
    Returns a click action dictionary.
    """
    return {
        "type": "click",
        "selector": selector
    }
