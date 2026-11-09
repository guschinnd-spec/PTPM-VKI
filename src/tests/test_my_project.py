# tests/test_my_project.py
import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from my_project import calculate_discount


class TestCalculateDiscount(unittest.TestCase):

    def test_vip_without_promo_gets_20_percent(self):
        self.assertEqual(calculate_discount(1000, "vip", False), 800.0)

    def test_regular_without_promo_gets_5_percent(self):
        self.assertEqual(calculate_discount(1000, "regular", False), 950.0)

    def test_new_customer_without_promo_no_discount(self):
        self.assertEqual(calculate_discount(1000, "new", False), 1000.0)

    def test_vip_with_promo_capped_at_30_percent(self):
        self.assertEqual(calculate_discount(1000, "vip", True), 700.0)

    def test_regular_with_promo_gets_15_percent(self):
        self.assertEqual(calculate_discount(1000, "regular", True), 850.0)

    def test_new_with_promo_gets_10_percent(self):
        self.assertEqual(calculate_discount(1000, "new", True), 900.0)

    def test_zero_price_returns_zero(self):
        self.assertEqual(calculate_discount(0, "vip", True), 0.0)

    def test_price_is_rounded_to_two_decimals(self):
        self.assertEqual(calculate_discount(99.99, "regular", False), 94.99)

    def test_large_price_is_processed(self):
        self.assertEqual(calculate_discount(1_000_000, "vip", False), 800_000.0)

    def test_unknown_customer_type_treated_as_new(self):
        self.assertEqual(calculate_discount(500, "unknown", False), 500.0)

    def test_exact_cap_boundary_30_percent(self):
        self.assertEqual(calculate_discount(100, "vip", True), 70.0)

    def test_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_discount(-100, "vip", False)

    def test_negative_price_message_contains_word(self):
        with self.assertRaisesRegex(ValueError, "отрицательн"):
            calculate_discount(-1, "regular", True)

    def test_returns_float(self):
        self.assertIsInstance(calculate_discount(100, "vip", True), float)

    def test_result_never_below_zero(self):
        self.assertGreaterEqual(calculate_discount(0.01, "vip", True), 0.0)

    def test_same_input_same_output(self):
        a = calculate_discount(777.77, "vip", True)
        b = calculate_discount(777.77, "vip", True)
        self.assertEqual(a, b)

    def test_result_less_than_or_equal_price(self):
        for price in (0, 1, 100, 9999.99):
            self.assertLessEqual(calculate_discount(price, "vip", True), price)

    def test_discount_never_negative_for_all_types(self):
        for ct in ("vip", "regular", "new", "other"):
            for promo in (True, False):
                self.assertGreaterEqual(calculate_discount(100, ct, promo), 0.0)

    def test_promo_adds_extra_discount(self):
        self.assertLess(
            calculate_discount(1000, "regular", True),
            calculate_discount(1000, "regular", False)
        )

    def test_vip_beats_regular(self):
        self.assertLess(
            calculate_discount(1000, "vip", False),
            calculate_discount(1000, "regular", False)
        )


if __name__ == "__main__":
    unittest.main()