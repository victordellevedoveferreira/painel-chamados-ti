import unittest

import pandas as pd

from src.metrics import calculate_metrics


class MetricsTest(unittest.TestCase):
    def test_summary(self) -> None:
        data = pd.DataFrame(
            {
                "category": ["Hardware", "Software", "Software"],
                "priority": ["Alta", "Media", "Baixa"],
                "year_month": ["2026-01", "2026-01", "2026-02"],
                "is_resolved": [True, True, False],
                "resolution_hours": [4.0, 12.0, None],
                "sla_met": [True, False, None],
                "satisfaction": [5.0, 3.0, None],
            }
        )
        metrics = calculate_metrics(data)
        self.assertEqual(metrics["summary"]["total_tickets"], 3)
        self.assertEqual(metrics["summary"]["open_tickets"], 1)
        self.assertEqual(metrics["summary"]["avg_resolution_hours"], 8.0)
        self.assertEqual(metrics["summary"]["sla_rate"], 50.0)
        self.assertEqual(metrics["summary"]["avg_satisfaction"], 4.0)


if __name__ == "__main__":
    unittest.main()

