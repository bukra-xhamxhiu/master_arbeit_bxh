# web_complexity_lab/exporters/csv_exporter.py
from typing import List, Dict, Any
import csv
from pathlib import Path


def _write_rows(path: Path, rows: List[Dict[str, Any]]):
    if not rows:
        return
    fieldnames = sorted(rows[0].keys())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_to_csv(all_app_results: List[Dict[str, Any]], out_dir: str):
    out = Path(out_dir)
    app_rows = []
    ui_rows = []
    test_rows = []
    log_rows = []
    agent_rows = []
    index_rows = []

    for r in all_app_results:
        app_rows.append(r["app_level"])
        ui_rows.extend(r["ui_metrics"])
        test_rows.extend(r["test_metrics"])
        log_rows.extend(r["log_metrics"])
        agent_rows.extend(r["agent_metrics"])
        index_rows.append(r["indices"])

    _write_rows(out / "apps_metrics.csv", app_rows)
    _write_rows(out / "ui_metrics.csv", ui_rows)
    _write_rows(out / "test_metrics.csv", test_rows)
    _write_rows(out / "log_metrics.csv", log_rows)
    _write_rows(out / "agent_metrics.csv", agent_rows)
    _write_rows(out / "complexity_indices.csv", index_rows)
