"""Ponto de entrada do pipeline completo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.dashboard import generate_dashboard
from src.etl import run_etl
from src.generate_data import generate_tickets
from src.metrics import calculate_metrics


ROOT = Path(__file__).resolve().parents[1]


def run(regenerate: bool = False, rows: int = 800) -> dict[str, object]:
    raw_path = ROOT / "data" / "raw" / "tickets.csv"
    processed_path = ROOT / "data" / "processed" / "tickets_clean.csv"
    database_path = ROOT / "data" / "database" / "support.db"
    metrics_path = ROOT / "docs" / "metrics.json"
    dashboard_path = ROOT / "docs" / "index.html"

    if regenerate or not raw_path.exists():
        generate_tickets(raw_path, rows=rows)
    data = run_etl(raw_path, processed_path, database_path)
    metrics = calculate_metrics(data)
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    generate_dashboard(data, dashboard_path)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa o pipeline de chamados de TI.")
    parser.add_argument("--regenerate", action="store_true", help="Recria a base sintetica.")
    parser.add_argument("--rows", type=int, default=800)
    args = parser.parse_args()
    metrics = run(regenerate=args.regenerate, rows=args.rows)
    summary = metrics["summary"]
    print("Pipeline concluido.")
    print(f"Chamados: {summary['total_tickets']}")
    print(f"SLA cumprido: {summary['sla_rate']}%")
    print(f"Dashboard: {ROOT / 'docs' / 'index.html'}")


if __name__ == "__main__":
    main()

