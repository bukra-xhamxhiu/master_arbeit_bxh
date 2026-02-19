# web_complexity_lab/collectors/ui_structure_collector.py
from typing import List, Dict, Any


class UIStructureCollector:
    """
    Collects static UI snapshots (DOM stats) for given start URLs.
    For now, assume snapshots already exist as JSON or you call Playwright here.
    """

    def __init__(self, app_config):
        self.app_config = app_config


def collect(self) -> List[Dict[str, Any]]:
        # Temporary dummy page-level data, just to test the pipeline
        return [
            {
                "page_id": "home",
                "url": self.app_config.base_url,
                "dom_node_count": 420,
                "interactive_elements": list(range(25)),  # pretend 25 controls
                "forms": [1, 2],  # pretend 2 forms
            },
            {
                "page_id": "details",
                "url": f"{self.app_config.base_url}/details/1",
                "dom_node_count": 580,
                "interactive_elements": list(range(30)),
                "forms": [1],
            },
        ]

"""
    def collect(self) -> List[Dict[str, Any]]:
        """
        Returns a list of UI states, e.g.:

        [
          {
            "page_id": "home",
            "url": "http://localhost:3000/",
            "dom_node_count": 450,
            "interactive_elements": [... raw info ...],
            "forms": [...],
          },
          ...
        ]
        """
        # TODO: integrate Playwright/driver or load precomputed JSON
        return []
"""