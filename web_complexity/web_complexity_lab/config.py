# web_complexity_lab/config.py
from dataclasses import dataclass, field
from typing import List, Dict, Any
import yaml


@dataclass
class AppConfig:
    id: str
    root_path: str
    base_url: str
    ui_structure: Dict[str, Any] = field(default_factory=dict)
    tests: Dict[str, Any] = field(default_factory=dict)
    logs: Dict[str, Any] = field(default_factory=dict)
    agents: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GlobalConfig:
    project_name: str
    applications: List[AppConfig]
    output: Dict[str, Any]


def load_config(path: str) -> GlobalConfig:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    apps = [
        AppConfig(
            id=a["id"],
            root_path=a["root_path"],
            base_url=a["base_url"],
            ui_structure=a.get("ui_structure", {}),
            tests=a.get("tests", {}),
            logs=a.get("logs", {}),
            agents=a.get("agents", {}),
        )
        for a in raw["applications"]
    ]

    return GlobalConfig(
        project_name=raw["project_name"],
        applications=apps,
        output=raw["output"],
    )
