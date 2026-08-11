"""Gera uma base sintetica e reproduzivel de chamados de suporte."""

from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


PRIORITIES = ["Crítica", "Alta", "Média", "Baixa"]
PRIORITY_WEIGHTS = [0.05, 0.20, 0.50, 0.25]
SLA_HOURS = {"Crítica": 4, "Alta": 8, "Média": 24, "Baixa": 48}
CATEGORIES = [
    "Acesso e senha",
    "Hardware",
    "Software",
    "Rede e VPN",
    "E-mail",
    "Videoconferência",
]
CATEGORY_WEIGHTS = [0.22, 0.18, 0.23, 0.15, 0.13, 0.09]
CHANNELS = ["Portal", "E-mail", "Telefone", "Presencial"]
LOCATIONS = ["Sede", "Unidade Norte", "Unidade Sul", "Remoto"]
ANALYSTS = ["Ana", "Bruno", "Carla", "Diego"]


def _random_datetime(rng: random.Random, start: datetime, end: datetime) -> datetime:
    seconds = int((end - start).total_seconds())
    return start + timedelta(seconds=rng.randint(0, seconds))


def _resolution_hours(rng: random.Random, priority: str) -> float:
    typical = {"Crítica": 3.0, "Alta": 6.0, "Média": 15.0, "Baixa": 30.0}
    value = max(0.4, rng.gauss(typical[priority], typical[priority] * 0.55))
    if rng.random() < 0.18:
        value *= rng.uniform(1.8, 3.2)
    return round(value, 2)


def generate_tickets(
    output_path: Path,
    rows: int = 800,
    seed: int = 42,
    start: datetime = datetime(2026, 1, 1, 8),
    end: datetime = datetime(2026, 6, 30, 18),
) -> Path:
    """Cria um CSV de chamados ficticios. Nenhum dado corporativo real e usado."""
    rng = random.Random(seed)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []
    for ticket_number in range(1, rows + 1):
        created_at = _random_datetime(rng, start, end)
        priority = rng.choices(PRIORITIES, PRIORITY_WEIGHTS, k=1)[0]
        category = rng.choices(CATEGORIES, CATEGORY_WEIGHTS, k=1)[0]
        is_resolved = rng.random() < 0.91

        if is_resolved:
            hours = _resolution_hours(rng, priority)
            resolved_at = created_at + timedelta(hours=hours)
            status = rng.choices(["Resolvido", "Fechado"], [0.35, 0.65], k=1)[0]
            sla_met = hours <= SLA_HOURS[priority]
            satisfaction = rng.choices(
                [1, 2, 3, 4, 5],
                [0.02, 0.04, 0.12, 0.35, 0.47] if sla_met else [0.08, 0.16, 0.30, 0.30, 0.16],
                k=1,
            )[0]
        else:
            resolved_at = ""
            status = "Em andamento"
            satisfaction = ""

        records.append(
            {
                "ticket_id": ticket_number,
                "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "resolved_at": resolved_at.strftime("%Y-%m-%d %H:%M:%S") if resolved_at else "",
                "category": category,
                "priority": priority,
                "channel": rng.choice(CHANNELS),
                "location": rng.choice(LOCATIONS),
                "analyst": rng.choice(ANALYSTS),
                "status": status,
                "satisfaction": satisfaction,
                "sla_hours": SLA_HOURS[priority],
            }
        )

    records.sort(key=lambda item: str(item["created_at"]))
    fieldnames = list(records[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera dados sinteticos de chamados de TI.")
    parser.add_argument("--rows", type=int, default=800)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("data/raw/tickets.csv"))
    args = parser.parse_args()
    path = generate_tickets(args.output, rows=args.rows, seed=args.seed)
    print(f"Dados gerados: {path} ({args.rows} chamados)")


if __name__ == "__main__":
    main()
