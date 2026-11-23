class Controller:
    def __init__(self, user_io, calculator, database, notifier):
        self.user_io = user_io
        self.calculator = calculator
        self.database = database
        self.notifier = notifier

    def run(self):
        a, b, c = self.user_io.get_input()
        cached = self.database.get(a, b, c)

        if cached is not None:
            triangle_type, error_message = cached
            source = "db"
        else:
            triangle_type, error_message = self.calculator.calculate(a, b, c)
            self.database.add(a, b, c, triangle_type, error_message)
            source = "calc"

        if error_message:
            result_str = f"Ошибка: {error_message}"
        else:
            result_str = f"Тип треугольника: {triangle_type}"

        self.notifier.send(result_str)
        return {
            "result": result_str,
            "source": source,
            "type": triangle_type,
            "error": error_message,
        }