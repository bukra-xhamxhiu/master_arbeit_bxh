# web_complexity_lab/collectors/log_parser.py
from typing import List, Dict, Any


class LogParser:
    """
    Parses execution logs (JUnit XML, Playwright traces, etc.)
    into normalized step-level timing and status.
    """

    def __init__(self, app_config):
        self.app_config = app_config

def collect(self) -> List[Dict[str, Any]]:
        # Single dummy log entry that corresponds to the test above
        return [
            {
                "test_id": "movies_open_and_search",
                "status": "passed",
                "duration_ms": 2100,
                "steps": [
                    {"step_index": 0, "duration_ms": 500, "status": "passed"},
                    {"step_index": 1, "duration_ms": 400, "status": "passed"},
                    {"step_index": 2, "duration_ms": 700, "status": "passed"},
                    {"step_index": 3, "duration_ms": 500, "status": "passed"},
                ],
                "retries": 0,
                "failures": [],
            }
        ]

        """
    def collect(self) -> List[Dict[str, Any]]:
        """
        Returns a list of log entries per test, e.g.:

        [
          {
            "test_id": "movies_add_twisters",
            "status": "passed",
            "duration_ms": 2300,
            "steps": [
              {"step_index": 0, "duration_ms": 300, "status": "passed"},
              ...
            ],
            "retries": 0,
            "failures": [],
          },
          ...
        ]
        """
        # TODO: parse junit xml / traces
        return []
"""