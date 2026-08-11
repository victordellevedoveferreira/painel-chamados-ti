import unittest

import pandas as pd

from src.etl import prepare_tickets


class PrepareTicketsTest(unittest.TestCase):
    def sample(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "ticket_id": 1,
                    "created_at": "2026-01-01 08:00:00",
                    "resolved_at": "2026-01-01 11:00:00",
                    "category": " Software ",
                    "priority": "Alta",
                    "channel": "Portal",
                    "location": "Sede",
                    "analyst": "Ana",
                    "status": "Resolvido",
                    "satisfaction": 5,
                    "sla_hours": 8,
                }
            ]
        )

    def test_calculates_resolution_and_sla(self) -> None:
        result = prepare_tickets(self.sample())
        self.assertEqual(result.loc[0, "category"], "Software")
        self.assertEqual(result.loc[0, "resolution_hours"], 3.0)
        self.assertTrue(bool(result.loc[0, "sla_met"]))
        self.assertEqual(result.loc[0, "year_month"], "2026-01")

    def test_rejects_missing_columns(self) -> None:
        with self.assertRaisesRegex(ValueError, "Colunas obrigatorias"):
            prepare_tickets(self.sample().drop(columns=["priority"]))

    def test_rejects_invalid_created_date(self) -> None:
        sample = self.sample()
        sample.loc[0, "created_at"] = "data-invalida"
        with self.assertRaisesRegex(ValueError, "Datas de abertura invalidas"):
            prepare_tickets(sample)


if __name__ == "__main__":
    unittest.main()

