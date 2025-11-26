"""
Unit tests for the utility calculator.

Run with: python -m unittest src.calculator.test
"""

import unittest

from . import calculate_utilities


class TestUtilityCalculator(unittest.TestCase):
    """Test cases for utility calculation functions."""

    def test_essential_efficiency_item(self):
        """Test calculation for an essential efficiency item (e.g., work laptop)."""
        # A $1000 laptop used 20 hours/week for 3 years
        laptop_data = {
            "item_name": "Work Laptop",
            "price": 1000.0,
            "income_level": "medium",
            "life_areas": ["career"],
            "necessity": "essential",
            "time_use": 20.0,
            "use_probability": "high",
            "life_span": 36,
            "category": "efficiency",
        }

        result = calculate_utilities(laptop_data)
        print(result)

        # Verify all expected keys are present
        self.assertIn("use_factor", result)
        self.assertIn("u_buy_useful", result)
        self.assertIn("u_buy_not_useful", result)
        self.assertIn("u_not_buy_useful", result)
        self.assertIn("u_not_buy_not_useful", result)

        # Verify use_factor is positive (hours per dollar)
        self.assertGreater(result["use_factor"], 0)

        # For essential items, buying when useful should be positive utility
        self.assertGreater(result["u_buy_useful"], 0)

        # Not buying when useful should have negative utility
        self.assertLess(result["u_not_buy_useful"], 0)

    def test_entertainment_item(self):
        """Test calculation for a nice-to-have entertainment item."""
        # A $500 gaming console used 10 hours/week for 5 years
        console_data = {
            "item_name": "Gaming Console",
            "price": 500.0,
            "income_level": "medium",
            "life_areas": ["personal"],
            "necessity": "nice_to_have",
            "time_use": 10.0,
            "use_probability": "medium",
            "life_span": 60,
            "category": "entertainment",
        }

        result = calculate_utilities(console_data)

        # Verify structure
        self.assertEqual(len(result), 5)

        # Use factor should be reasonable (total hours / price)
        # 10 hrs/week * 52 weeks * 5 years * 0.6 probability / $500
        expected_use_factor = (10 * 52 * 5 * 0.6) / 500
        self.assertAlmostEqual(result["use_factor"], expected_use_factor, places=2)

        # Buying when not useful should be negative
        self.assertLess(result["u_buy_not_useful"], 0)

    def test_health_item_low_income(self):
        """Test calculation for a health item with low income level."""
        # A $200 fitness tracker used 2 hours/week for 2 years
        fitness_data = {
            "item_name": "Fitness Tracker",
            "price": 200.0,
            "income_level": "low",
            "life_areas": ["health"],
            "necessity": "nice_to_have",
            "time_use": 2.0,
            "use_probability": "high",
            "life_span": 24,
            "category": "qol",
        }

        result = calculate_utilities(fitness_data)
        print(result)

        # For low income, the cost penalty should be significant
        # Buying when not useful should have strong negative utility
        self.assertLess(result["u_buy_not_useful"], -1000)

        # Use factor calculation
        expected_hours = 2 * 52 * 2 * 0.9  # weekly * weeks/year * years * probability
        expected_use_factor = expected_hours / 200
        self.assertAlmostEqual(result["use_factor"], expected_use_factor, places=2)


if __name__ == "__main__":
    unittest.main()
