from calc import TriangleCalculator
from db import TriangleDatabase
from ui import ConsoleUserIO
from external import EmailNotifier
from controller import Controller


def main():
    # Если запускаете как скрипт из папки src
    db = TriangleDatabase("triangles.db")  # файл БД
    controller = Controller(
        user_io=ConsoleUserIO(),
        calculator=TriangleCalculator(),
        database=db,
        notifier=EmailNotifier(),
    )
    result = controller.run()
    print("Результат:", result["result"])
    db.close()


if __name__ == "__main__":
    main()