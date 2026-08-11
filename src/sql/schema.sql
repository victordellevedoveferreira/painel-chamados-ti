DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    category TEXT NOT NULL,
    priority TEXT NOT NULL,
    channel TEXT NOT NULL,
    location TEXT NOT NULL,
    analyst TEXT NOT NULL,
    status TEXT NOT NULL,
    satisfaction REAL,
    sla_hours REAL NOT NULL,
    is_resolved INTEGER NOT NULL,
    resolution_hours REAL,
    sla_met INTEGER,
    year_month TEXT NOT NULL,
    created_date TEXT NOT NULL
);

