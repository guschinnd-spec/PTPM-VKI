class TriangleCalculator:
    """Определяет тип треугольника по длинам сторон."""

    def calculate(self, a, b, c):
        if not all(isinstance(x, (int, float)) for x in (a, b, c)):
            return None, "Стороны должны быть числами"
        if a <= 0 or b <= 0 or c <= 0:
            return None, "Стороны должны быть положительными"
        if a + b <= c or a + c <= b or b + c <= a:
            return None, "Треугольник с такими сторонами не существует"

        sides = sorted([a, b, c])
        if sides[0] == sides[1] == sides[2]:
            return "равносторонний", None
        if sides[0] == sides[1] or sides[1] == sides[2]:
            return "равнобедренный", None
        if abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 1e-9:
            return "прямоугольный", None
        return "разносторонний", None