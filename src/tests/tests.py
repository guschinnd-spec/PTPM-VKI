import unittest
from unittest.mock import patch, MagicMock

# Подстраиваем пути импорта под вашу структуру
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.calc import TriangleCalculator
from src.db import TriangleDatabase
from src.external import EmailNotifier
from src.controller import Controller


# ==================== UNIT-ТЕСТЫ (2 шт.) ====================
class TestCalculatorUnit(unittest.TestCase):
    def setUp(self):
        self.calc = TriangleCalculator()

    def test_negative_side(self):
        t, err = self.calc.calculate(-1, 2, 2)
        self.assertIsNone(t)
        self.assertEqual(err, "Стороны должны быть положительными")

    def test_non_numeric(self):
        t, err = self.calc.calculate("a", 2, 2)
        self.assertIsNone(t)
        self.assertEqual(err, "Стороны должны быть числами")


class TestDatabaseUnit(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_crud(self):
        self.db.add(3, 4, 5, "прямоугольный", None)
        self.assertEqual(self.db.get(3, 4, 5), ("прямоугольный", None))
        self.db.delete(3, 4, 5)
        self.assertIsNone(self.db.get(3, 4, 5))


# ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ (3 шт.) ====================
class TestControllerIntegration(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def _make_controller(self, user_io, notifier=None):
        return Controller(
            user_io=user_io,
            calculator=TriangleCalculator(),
            database=self.db,
            notifier=notifier or EmailNotifier(),
        )

    def test_full_scenario_calc_and_persist(self):
        fake_io = MagicMock()
        fake_io.get_input.return_value = (3, 4, 5)
        fake_notifier = MagicMock()
        fake_notifier.send.return_value = True

        controller = self._make_controller(fake_io, fake_notifier)
        result = controller.run()

        self.assertEqual(result["source"], "calc")
        self.assertEqual(result["type"], "прямоугольный")
        self.assertEqual(self.db.get(3, 4, 5), ("прямоугольный", None))
        fake_notifier.send.assert_called_once_with("Тип треугольника: прямоугольный")

    @patch("src.controller.TriangleCalculator.calculate")
    def test_second_call_uses_cache(self, mock_calc):
        mock_calc.return_value = ("равносторонний", None)
        fake_io = MagicMock()
        fake_io.get_input.return_value = (5, 5, 5)
        fake_notifier = MagicMock()
        fake_notifier.send.return_value = True

        controller = self._make_controller(fake_io, fake_notifier)
        r1 = controller.run()
        r2 = controller.run()

        self.assertEqual(r1["source"], "calc")
        self.assertEqual(r2["source"], "db")
        self.assertEqual(mock_calc.call_count, 1)
        self.assertEqual(fake_notifier.send.call_count, 2)

    def test_error_scenario(self):
        fake_io = MagicMock()
        fake_io.get_input.return_value = (1, 1, 10)
        fake_notifier = MagicMock()
        fake_notifier.send.return_value = True

        controller = self._make_controller(fake_io, fake_notifier)
        result = controller.run()

        self.assertIn("Ошибка", result["result"])
        self.assertEqual(result["error"], "Треугольник с такими сторонами не существует")
        self.assertEqual(self.db.get(1, 1, 10), (None, "Треугольник с такими сторонами не существует"))
        fake_notifier.send.assert_called_once_with("Ошибка: Треугольник с такими сторонами не существует")


if __name__ == "__main__":
    unittest.main()