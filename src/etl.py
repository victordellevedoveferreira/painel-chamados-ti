"""Limpeza, validacao e carga dos chamados em CSV e SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "ticket_id",
    "created_at",
    "resolved_at",
    "category",
    "priority",
    "channel",
    "location",
    "analyst",
    "status",
    "satisfaction",
    "sla_hours",
}


def prepare_tickets(raw: pd.DataFrame) -> pd.DataFrame:
    """Valida e transforma a base bruta em uma tabela analitica."""
    missing = REQUIRED_COLUMNS - set(raw.columns)
    if missing:
        raise ValueError(f"Colunas obrigatorias ausentes: {sorted(missing)}")

    data = raw.copy()
    text_columns = ["category", "priority", "channel", "location", "analyst", "status"]
    for column in text_columns:
        data[column] = data[column].astype("string").str.strip()

    data["created_at"] = pd.to_datetime(data["created_at"], errors="coerce")
    data["resolved_at"] = pd.to_datetime(data["resolved_at"], errors="coerce")
    if data["created_at"].isna().any():
        bad_rows = data.index[data["created_at"].isna()].tolist()
        raise ValueError(f"Datas de abertura invalidas nas linhas: {bad_rows[:10]}")

    data["ticket_id"] = pd.to_numeric(data["ticket_id"], errors="raise").astype(int)
    data["sla_hours"] = pd.to_numeric(data["sla_hours"], errors="raise").astype(float)
    data["satisfaction"] = pd.to_numeric(data["satisfaction"], errors="coerce")
    data["is_resolved"] = data["resolved_at"].notna()
    data["resolution_hours"] = (
        (data["resolved_at"] - data["created_at"]).dt.total_seconds() / 3600
    ).round(2)
    data["sla_met"] = (data["resolution_hours"] <= data["sla_hours"]).where(data["is_resolved"])
    data["year_month"] = data["created_at"].dt.strftime("%Y-%m")
    data["created_date"] = data["created_at"].dt.strftime("%Y-%m-%d")

    if data["ticket_id"].duplicated().any():
        raise ValueError("Existem ticket_id duplicados na base.")
    if (data["resolution_hours"].dropna() < 0).any():
        raise ValueError("Existem chamados resolvidos antes da abertura.")

    return data.sort_values(["created_at", "ticket_id"]).reset_index(drop=True)


def load_to_sqlite(data: pd.DataFrame, database_path: Path) -> None:
    """Carrega a tabela tratada em SQLite e cria indices de consulta."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        data.to_sql("tickets", connection, if_exists="replace", index=False)
        connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_tickets_id ON tickets(ticket_id)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_tickets_month ON tickets(year_month)")


def run_etl(raw_path: Path, processed_path: Path, database_path: Path) -> pd.DataFrame:
    """Executa o fluxo CSV bruto -> tabela tratada -> SQLite."""
    raw = pd.read_csv(raw_path)
    data = prepare_tickets(raw)
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(processed_path, index=False, date_format="%Y-%m-%d %H:%M:%S")
    load_to_sqlite(data, database_path)
    return data

