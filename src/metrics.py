"""Calculo de indicadores para o dashboard de chamados."""

from __future__ import annotations

from typing import Any

import pandas as pd


def _round_or_zero(value: float, digits: int = 1) -> float:
    return round(float(value), digits) if pd.notna(value) else 0.0


def calculate_metrics(data: pd.DataFrame) -> dict[str, Any]:
    """Retorna KPIs e agregacoes em tipos serializaveis como JSON."""
    total = int(len(data))
    resolved = data[data["is_resolved"]].copy()
    resolved_count = int(len(resolved))

    summary = {
        "total_tickets": total,
        "resolved_tickets": resolved_count,
        "open_tickets": total - resolved_count,
        "resolution_rate": _round_or_zero((resolved_count / total * 100) if total else 0),
        "avg_resolution_hours": _round_or_zero(resolved["resolution_hours"].mean()),
        "sla_rate": _round_or_zero(resolved["sla_met"].astype(float).mean() * 100 if resolved_count else 0),
        "avg_satisfaction": _round_or_zero(resolved["satisfaction"].mean(), 2),
    }

    categories: list[dict[str, Any]] = []
    for category, group in data.groupby("category", sort=False):
        group_resolved = group[group["is_resolved"]]
        categories.append(
            {
                "category": str(category),
                "total": int(len(group)),
                "avg_resolution_hours": _round_or_zero(group_resolved["resolution_hours"].mean()),
                "sla_rate": _round_or_zero(
                    group_resolved["sla_met"].astype(float).mean() * 100 if len(group_resolved) else 0
                ),
            }
        )
    categories.sort(key=lambda item: item["total"], reverse=True)

    monthly: list[dict[str, Any]] = []
    for month, group in data.groupby("year_month", sort=True):
        group_resolved = group[group["is_resolved"]]
        monthly.append(
            {
                "month": str(month),
                "total": int(len(group)),
                "sla_rate": _round_or_zero(
                    group_resolved["sla_met"].astype(float).mean() * 100 if len(group_resolved) else 0
                ),
            }
        )

    priorities = [
        {"priority": str(priority), "total": int(len(group))}
        for priority, group in data.groupby("priority", sort=False)
    ]
    priorities.sort(key=lambda item: item["total"], reverse=True)

    return {"summary": summary, "categories": categories, "monthly": monthly, "priorities": priorities}

