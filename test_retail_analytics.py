import unittest

from generate_data import create_sales_data
from retail_analytics import filter_sales, monthly_revenue, summary_metrics


class RetailAnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.sales = create_sales_data(rows=100, seed=7)

    def test_generated_data_is_reproducible_and_valid(self):
        repeated = create_sales_data(rows=100, seed=7)
        self.assertTrue(self.sales.equals(repeated))
        self.assertEqual(len(self.sales), 100)
        self.assertTrue((self.sales["revenue"] >= 0).all())

    def test_filters_and_metrics_match_selected_rows(self):
        category = self.sales["category"].iloc[0]
        selected = filter_sales(self.sales, "2024-01-01", "2025-12-31", [category], [])
        metrics = summary_metrics(selected)
        self.assertTrue((selected["category"] == category).all())
        self.assertAlmostEqual(metrics["revenue"], selected["revenue"].sum())
        self.assertEqual(metrics["orders"], selected["order_id"].nunique())

    def test_monthly_revenue_sums_to_total(self):
        monthly = monthly_revenue(self.sales)
        self.assertAlmostEqual(monthly["revenue"].sum(), self.sales["revenue"].sum())


if __name__ == "__main__":
    unittest.main()