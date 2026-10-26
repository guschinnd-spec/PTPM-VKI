import logging
import math

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("triangle.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def calculate_triangle(side_a_str: str, side_b_str: str, side_c_str: str) -> tuple[str, list[tuple[int, int]]]:
    logging.info(f"Входные данные: A='{side_a_str}', B='{side_b_str}', C='{side_c_str}'")

    # 1. Валидация на числа
    try:
        a = float(side_a_str)
        b = float(side_b_str)
        c = float(side_c_str)
    except ValueError:
        logging.error("Ошибка: Входные данные не являются числами.")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    # 2. Проверка на положительные числа и неравенство треугольника
    if a <= 0 or b <= 0 or c <= 0:
        logging.warning("Ошибка: Стороны должны быть больше нуля.")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        logging.warning("Ошибка: Нарушено неравенство треугольника.")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    # 3. Определение типа
    is_ab = math.isclose(a, b)
    is_bc = math.isclose(b, c)
    is_ac = math.isclose(a, c)

    if is_ab and is_bc:
        triangle_type = "равносторонний"
    elif is_ab or is_bc or is_ac:
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    logging.info(f"Тип: {triangle_type}")

    # 4. Расчет координат для сетки 100x100
    x1, y1 = 0.0, 0.0
    x2, y2 = c, 0.0

    cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
    cos_A = max(-1.0, min(1.0, cos_A))
    sin_A = math.sin(math.acos(cos_A))

    x3 = b * cos_A
    y3 = b * sin_A

    max_coord = max(x2, x3, y3)
    scale = 90.0 / max_coord if max_coord > 0 else 1.0

    coords = [
        (int(round(x1 * scale)) + 5, int(round(y1 * scale)) + 5),
        (int(round(x2 * scale)) + 5, int(round(y2 * scale)) + 5),
        (int(round(x3 * scale)) + 5, int(round(y3 * scale)) + 5)
    ]

    logging.info(f"Координаты: {coords}")
    return triangle_type, coords
