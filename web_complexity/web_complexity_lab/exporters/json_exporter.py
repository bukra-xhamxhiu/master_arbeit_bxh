# web_complexity_lab/exporters/json_exporter.py
from typing import List, Dict, Any
from pathlib import Path
import json


def export_to_json(all_app_results: List[Dict[str, Any]], out_dir: str) -> None:
    """
    Writes the full structured result plus convenient per-entity JSON files.

    Layout:
      out_dir/
        results_full.json              # everything
        apps_metrics.json              # list of per-app aggregates
        ui_metrics.json                # list of per-page/per-state UI metrics
        test_metrics.json              # list of per-test metrics
        log_metrics.json               # list of per-test log metrics
        agent_metrics.json             # list of per-episode agent metrics
        complexity_indices.json        # list of per-app indices
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # 1) Full object (debug / research use)
    full_path = out / "results_full.json"
    with full_path.open("w", encoding="utf-8") as f:
        json.dump(all_app_results, f, ensure_ascii=False, indent=2)

    # 2) Split views for easier analysis
    app_rows: List[Dict[str, Any]] = []
    ui_rows: List[Dict[str, Any]] = []
    test_rows: List[Dict[str, Any]] = []
    log_rows: List[Dict[str, Any]] = []
    agent_rows: List[Dict[str, Any]] = []
    index_rows: List[Dict[str, Any]] = []

    for r in all_app_results:
        app_rows.append(r["app_level"])
        ui_rows.extend(r["ui_metrics"])
        test_rows.extend(r["test_metrics"])
        log_rows.extend(r["log_metrics"])
        agent_rows.extend(r["agent_metrics"])
        index_rows.append(r["indices"])

    def _dump(path: Path, obj: Any) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)

    _dump(out / "apps_metrics.json", app_rows)
    _dump(out / "ui_metrics.json", ui_rows)
    _dump(out / "test_metrics.json", test_rows)
    _dump(out / "log_metrics.json", log_rows)
    _dump(out / "agent_metrics.json", agent_rows)
    _dump(out / "complexity_indices.json", index_rows)
