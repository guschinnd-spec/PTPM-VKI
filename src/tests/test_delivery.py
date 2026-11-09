import unittest
import sys, os
# Эта строка нужна, чтобы Python нашел папку src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from delivery_service import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):

    # --- 1. ОШИБКИ И ГРАНИЦЫ ---
    def test_invalid_weight_too_light(self):
        self.assertEqual(calculate_delivery_cost(0.05, 100, "обычный"), (-1, "0000-00-00"))

    def test_invalid_weight_too_heavy(self):
        self.assertEqual(calculate_delivery_cost(60, 100, "обычный"), (-1, "0000-00-00"))

    def test_invalid_distance_zero(self):
        self.assertEqual(calculate_delivery_cost(10, 0, "обычный"), (-1, "0000-00-00"))

    def test_invalid_package_type(self):
        self.assertEqual(calculate_delivery_cost(10, 100, "стекло"), (-1, "0000-00-00"))

    def test_boundary_weight_50kg(self):
        self.assertNotEqual(calculate_delivery_cost(50, 100, "обычный")[0], -1)

    def test_boundary_distance_5000km(self):
        self.assertNotEqual(calculate_delivery_cost(5, 5000, "обычный")[0], -1)

    # --- 2. РАСЧЕТ СТОИМОСТИ (ВЕТКИ ВЕСА) ---
    def test_base_cost_no_multiplier(self):
        # 200 + (100*5) = 700
        self.assertEqual(calculate_delivery_cost(5, 100, "обычный")[0], 700)

    def test_weight_multiplier_1_2(self): # БАГ 1
        # Вес 10 кг (от 5 до 20). Должно быть 700 * 1.2 = 840
        self.assertEqual(calculate_delivery_cost(10, 100, "обычный")[0], 840)

    def test_weight_multiplier_1_5(self):
        # Вес 20 кг. 700 * 1.5 = 1050
        self.assertEqual(calculate_delivery_cost(20, 100, "обычный")[0], 1050)

    # --- 3. ТИПЫ ПОСЫЛОК ---
    def test_fragile_adds_300(self):
        self.assertEqual(calculate_delivery_cost(5, 100, "хрупкий")[0], 1000)

    def test_dangerous_adds_1000(self):
        self.assertEqual(calculate_delivery_cost(5, 100, "опасный")[0], 1700)

    # --- 4. ЭКСПРЕСС ---
    def test_express_multiplier(self): # БАГ 2
        # Обычная цена 700. Экспресс должен быть дороже! Ждем 1050 (700 * 1.5)
        self.assertEqual(calculate_delivery_cost(5, 100, "обычный", is_express=True)[0], 1050)

    # --- 5. ДАТА ДОСТАВКИ ---
    def test_delivery_date_standard(self):
        # 500 / 500 = 1 день. 03.09 + 1 = 04.09
        self.assertEqual(calculate_delivery_cost(5, 500, "обычный")[1], "2026-09-04")

    def test_delivery_date_long_distance(self):
        # 1500 / 500 = 3 дня. 03.09 + 3 = 06.09
        self.assertEqual(calculate_delivery_cost(5, 1500, "обычный")[1], "2026-09-06")

    def test_delivery_date_express(self): # БАГ 3
        # 1000 км = 2 дня. Экспресс: 2 // 2 = 1 день. 03.09 + 1 = 04.09
        self.assertEqual(calculate_delivery_cost(5, 1000, "обычный", is_express=True)[1], "2026-09-04")

    def test_delivery_date_express_short(self): # БАГ 4
        # 400 км = 1 день. Экспресс: 1 // 2 = 0 дней! Дата не должна быть 03.09. Ждем минимум 04.09.
        self.assertEqual(calculate_delivery_cost(5, 400, "обычный", is_express=True)[1], "2026-09-04")

    def test_minimum_delivery_days(self):
        # 1 км. max(1, 1//500) = 1 день. 04.09
        self.assertEqual(calculate_delivery_cost(5, 1, "обычный")[1], "2026-09-04")

    # --- 6. ФОРМАТ И ТИПЫ ---
    def test_returns_tuple(self):
        self.assertIsInstance(calculate_delivery_cost(5, 100, "обычный"), tuple)

    def test_returns_integer_cost(self):
        self.assertIsInstance(calculate_delivery_cost(5, 100, "обычный")[0], int)

    def test_return_date_format(self):
        self.assertRegex(calculate_delivery_cost(5, 100, "обычный")[1], r"^\d{4}-\d{2}-\d{2}$")


if __name__ == "__main__":
    unittest.main()