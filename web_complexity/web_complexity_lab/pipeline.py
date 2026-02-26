# web_complexity_lab/pipeline.py
from typing import Dict, Any

from .collectors.ui_structure_collector import UIStructureCollector
from .collectors.test_parser import TestParser
from .collectors.log_parser import LogParser
from .collectors.agent_log_parser import AgentLogParser

from .features.ui_metrics import compute_ui_metrics
from .features.test_metrics import compute_test_metrics
from .features.log_metrics import compute_log_metrics
from .features.agent_metrics import compute_agent_metrics
from .features.aggregation import aggregate_per_app

from .models.complexity_index import compute_complexity_indices
from .exporters.csv_exporter import export_to_csv
from .exporters.json_exporter import export_to_json
from .exporters.html_exporter import export_to_html


def run_evaluation(cfg) -> None:
    all_app_results = []

    for app in cfg.applications:
        print(f"=== Evaluating application: {app.id} ===")

        ui_structure_collector = UIStructureCollector(app)
        raw_ui_states = ui_structure_collector.collect()

        test_parser = TestParser(app)
        raw_tests = test_parser.collect()

        log_parser = LogParser(app)
        raw_logs = log_parser.collect()

        agent_parser = AgentLogParser(app)
        raw_agent_logs = agent_parser.collect()

#compute metrics and indexes
        ui_metrics = compute_ui_metrics(app.id, raw_ui_states)
        test_metrics = compute_test_metrics(app.id, raw_tests)
        log_metrics = compute_log_metrics(app.id, raw_logs)
        agent_metrics = compute_agent_metrics(app.id, raw_agent_logs)

        app_level = aggregate_per_app(
            app_id=app.id,
            ui_metrics=ui_metrics,
            test_metrics=test_metrics,
            log_metrics=log_metrics,
            agent_metrics=agent_metrics,
        )

        indices = compute_complexity_indices(app_level)

        result = {
            "app_id": app.id,
            "ui_metrics": ui_metrics,
            "test_metrics": test_metrics,
            "log_metrics": log_metrics,
            "agent_metrics": agent_metrics,
            "app_level": app_level,
            "indices": indices,
        }
        all_app_results.append(result)

    out_dir = cfg.output["dir"]
    formats = cfg.output.get("formats", ["csv"])

    for fmt in formats:
        if fmt == "csv":
            export_to_csv(all_app_results, out_dir)
        elif fmt == "json":
            export_to_json(all_app_results, out_dir)
        elif fmt == "html":
            export_to_html(all_app_results, out_dir)
