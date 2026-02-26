# web_complexity_lab/exporters/html_exporter.py
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime


def export_to_html(all_app_results: List[Dict[str, Any]], out_dir: str) -> None:
    """
    Generates an HTML report with complexity metrics and visualizations.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    html_content = _generate_html_report(all_app_results)

    report_path = out / "complexity_report.html"
    with report_path.open("w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML report generated: {report_path}")


def _generate_html_report(all_app_results: List[Dict[str, Any]]) -> str:
    """Generate the full HTML report."""

    # Extract data for the report
    apps_data = []
    for r in all_app_results:
        apps_data.append({
            "app_id": r["app_id"],
            "app_level": r["app_level"],
            "indices": r["indices"],
            "ui_metrics": r["ui_metrics"],
            "test_metrics": r["test_metrics"],
            "agent_metrics": r["agent_metrics"],
        })

    # TU Chemnitz green: #007A33 or similar
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Complexity Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #ffffff;
            color: #333333;
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 3px solid #007A33;
        }}
        h1 {{
            font-size: 2rem;
            color: #007A33;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        .subtitle {{
            color: #666;
            font-size: 1rem;
        }}
        .institution {{
            margin-top: 1rem;
            color: #007A33;
            font-weight: 500;
        }}
        .timestamp {{
            color: #888;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .app-card {{
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .app-card:hover {{
            box-shadow: 0 4px 12px rgba(0,122,51,0.15);
        }}
        .app-name {{
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #007A33;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #007A33;
        }}
        .wcs-score {{
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            margin: 1rem 0;
            color: #007A33;
        }}
        .wcs-label {{
            text-align: center;
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }}
        .indices-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.5rem;
        }}
        .index-item {{
            background: #f8f9fa;
            padding: 0.6rem;
            border-radius: 4px;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        .index-name {{
            font-size: 0.75rem;
            color: #666;
            margin-bottom: 0.2rem;
        }}
        .index-value {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
        }}
        .section {{
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        h2 {{
            font-size: 1.3rem;
            margin-bottom: 1rem;
            color: #007A33;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #007A33;
        }}
        h3 {{
            font-size: 1.1rem;
            margin: 1.5rem 0 1rem;
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }}
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        th {{
            background: #007A33;
            color: white;
            font-weight: 500;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .bar-container {{
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
        }}
        .bar {{
            height: 100%;
            border-radius: 4px;
            background: #007A33;
        }}
        .bar-light {{
            background: #4CAF50;
        }}
        .comparison-chart {{
            display: flex;
            align-items: flex-end;
            justify-content: center;
            gap: 3rem;
            height: 220px;
            padding: 1.5rem;
            background: #f8f9fa;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        .chart-bar {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100px;
        }}
        .chart-bar-inner {{
            width: 70px;
            background: linear-gradient(180deg, #007A33, #4CAF50);
            border-radius: 4px 4px 0 0;
        }}
        .chart-label {{
            margin-top: 0.5rem;
            font-size: 0.85rem;
            text-align: center;
            color: #333;
        }}
        .chart-value {{
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #007A33;
        }}
        .metric-row {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.5rem;
        }}
        .metric-label {{
            width: 60px;
            font-size: 0.85rem;
            color: #666;
        }}
        .metric-value {{
            width: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            text-align: right;
        }}
        footer {{
            text-align: center;
            padding: 2rem;
            color: #666;
            font-size: 0.85rem;
            border-top: 1px solid #e0e0e0;
            margin-top: 2rem;
        }}
        .legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            margin-top: 1rem;
            justify-content: center;
            font-size: 0.85rem;
            color: #666;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .legend-color {{
            width: 14px;
            height: 14px;
            border-radius: 2px;
            background: #007A33;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Web Complexity Analysis Report</h1>
            <p class="subtitle">UI Complexity Evaluation from Tests &amp; Agent Logs</p>
            <p class="institution">Technical University of Chemnitz</p>
            <p class="timestamp">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </header>

        <section class="summary-grid">
            {_generate_app_cards(apps_data)}
        </section>

        <section class="section">
            <h2>Complexity Score Comparison</h2>
            {_generate_comparison_chart(apps_data)}
            <div class="legend">
                <div class="legend-item"><span class="legend-color"></span> SUCI - Structural UI Complexity</div>
                <div class="legend-item"><span class="legend-color"></span> IFCI - Interaction Flow Complexity</div>
                <div class="legend-item"><span class="legend-color"></span> TCI - Temporal Complexity</div>
                <div class="legend-item"><span class="legend-color"></span> ADI - Agent Difficulty Index</div>
            </div>
        </section>

        <section class="section">
            <h2>Detailed Metrics</h2>
            {_generate_metrics_tables(apps_data)}
        </section>

        <footer>
            <p><strong>Web Complexity Lab</strong></p>
            <p>Master Thesis Project - Technical University of Chemnitz</p>
            <p>December 2025</p>
        </footer>
    </div>
</body>
</html>"""

    return html


def _generate_app_cards(apps_data: List[Dict]) -> str:
    """Generate summary cards for each app."""
    cards = []
    for app in apps_data:
        indices = app["indices"]
        wcs = indices.get("wcs", 0)

        card = f"""
        <div class="app-card">
            <div class="app-name">{app["app_id"].replace("_", " ").title()}</div>
            <div class="wcs-score">{wcs:.3f}</div>
            <div class="wcs-label">Weighted Complexity Score (WCS)</div>
            <div class="indices-grid">
                <div class="index-item">
                    <div class="index-name">SUCI</div>
                    <div class="index-value">{indices.get("suci", 0):.3f}</div>
                </div>
                <div class="index-item">
                    <div class="index-name">IFCI</div>
                    <div class="index-value">{indices.get("ifci", 0):.3f}</div>
                </div>
                <div class="index-item">
                    <div class="index-name">TCI</div>
                    <div class="index-value">{indices.get("trci", 0):.3f}</div>
                </div>
                <div class="index-item">
                    <div class="index-name">ADI</div>
                    <div class="index-value">{indices.get("adi", 0):.3f}</div>
                </div>
            </div>
        </div>"""
        cards.append(card)

    return "\n".join(cards)


def _generate_comparison_chart(apps_data: List[Dict]) -> str:
    """Generate visual comparison chart."""
    max_wcs = max(app["indices"].get("wcs", 0) for app in apps_data) or 1

    bars = []
    for app in apps_data:
        wcs = app["indices"].get("wcs", 0)
        height = int((wcs / max_wcs) * 160)

        bars.append(f"""
        <div class="chart-bar">
            <div class="chart-value">{wcs:.3f}</div>
            <div class="chart-bar-inner" style="height: {height}px;"></div>
            <div class="chart-label">{app["app_id"].replace("_", " ").title()}</div>
        </div>""")

    return f'<div class="comparison-chart">{"".join(bars)}</div>'


def _generate_metrics_tables(apps_data: List[Dict]) -> str:
    """Generate detailed metrics tables."""
    tables = []

    for app in apps_data:
        app_level = app["app_level"]
        indices = app["indices"]

        table = f"""
        <h3>{app["app_id"].replace("_", " ").title()}</h3>
        <table>
            <tr>
                <th>Category</th>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td rowspan="3">UI Structure</td>
                <td>Total Pages</td>
                <td>{app_level.get("total_pages", 0)}</td>
            </tr>
            <tr>
                <td>Avg DOM Nodes</td>
                <td>{app_level.get("avg_dom_nodes", 0):,.0f}</td>
            </tr>
            <tr>
                <td>Avg Interactive Elements</td>
                <td>{app_level.get("avg_interactive_count", 0):.1f}</td>
            </tr>
            <tr>
                <td rowspan="4">Test Coverage</td>
                <td>Total Tests</td>
                <td>{app_level.get("total_tests", 0)}</td>
            </tr>
            <tr>
                <td>Avg Steps per Test</td>
                <td>{app_level.get("avg_test_steps", 0):.1f}</td>
            </tr>
            <tr>
                <td>Total Clicks</td>
                <td>{app_level.get("total_clicks", 0)}</td>
            </tr>
            <tr>
                <td>Total Assertions</td>
                <td>{app_level.get("total_assertions", 0)}</td>
            </tr>
            <tr>
                <td rowspan="2">Agent Metrics</td>
                <td>Total Episodes</td>
                <td>{app_level.get("total_episodes", 0)}</td>
            </tr>
            <tr>
                <td>Avg Steps to Success</td>
                <td>{app_level.get("avg_agent_steps_to_success", 0):.1f}</td>
            </tr>
        </table>

        <div style="margin: 1rem 0;">
            <div class="metric-row">
                <span class="metric-label">SUCI</span>
                <div class="bar-container" style="flex: 1;">
                    <div class="bar" style="width: {indices.get('suci', 0) * 100}%;"></div>
                </div>
                <span class="metric-value">{indices.get('suci', 0):.3f}</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">IFCI</span>
                <div class="bar-container" style="flex: 1;">
                    <div class="bar bar-light" style="width: {indices.get('ifci', 0) * 100}%;"></div>
                </div>
                <span class="metric-value">{indices.get('ifci', 0):.3f}</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">TCI</span>
                <div class="bar-container" style="flex: 1;">
                    <div class="bar" style="width: {indices.get('trci', 0) * 100}%;"></div>
                </div>
                <span class="metric-value">{indices.get('trci', 0):.3f}</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">ADI</span>
                <div class="bar-container" style="flex: 1;">
                    <div class="bar bar-light" style="width: {indices.get('adi', 0) * 100}%;"></div>
                </div>
                <span class="metric-value">{indices.get('adi', 0):.3f}</span>
            </div>
            <div class="metric-row" style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #e0e0e0;">
                <span class="metric-label"><strong>WCS</strong></span>
                <div class="bar-container" style="flex: 1;">
                    <div class="bar" style="width: {indices.get('wcs', 0) * 100}%;"></div>
                </div>
                <span class="metric-value"><strong>{indices.get('wcs', 0):.3f}</strong></span>
            </div>
        </div>
        """
        tables.append(table)

    return "\n".join(tables)
