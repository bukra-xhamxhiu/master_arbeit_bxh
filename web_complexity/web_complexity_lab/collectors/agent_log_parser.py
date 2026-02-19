# web_complexity_lab/collectors/agent_log_parser.py
from typing import List, Dict, Any


class AgentLogParser:
    """
    Parses UI agent (RL / LLM) logs, e.g. JSONL with episodes.
    """

    def __init__(self, app_config):
        self.app_config = app_config

        class AgentLogParser:
    def __init__(self, app_config):
        self.app_config = app_config

    def collect(self) -> List[Dict[str, Any]]:
        # Dummy agent episode for the same "search movie" task
        return [
            {
                "episode_id": "ep_0001",
                "task_id": "search_movie_twisters",
                "success": True,
                "steps": [
                    {"action": "navigate", "selector": None},
                    {"action": "click", "selector": "text=Movies"},
                    {"action": "click", "selector": "#search"},
                    {"action": "type", "selector": "#search"},
                    {"action": "click", "selector": "text=Search"},
                ],
                "backtracks": 1,
            }
        ]


"""
    def collect(self) -> List[Dict[str, Any]]:
        """
        Returns a list of episodes, e.g.:

        [
          {
            "episode_id": "ep_001",
            "task_id": "search_movie_twisters",
            "success": True,
            "steps": [
              {"action": "click", "selector": "text=Movies", "reward": 0.1},
              ...
            ],
          },
          ...
        ]
        """
        # TODO: load JSONL agent logs
        return []
"""