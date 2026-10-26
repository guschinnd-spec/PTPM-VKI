from triangel import calculate_triangle

def main():
    print("--- Расчет параметров треугольника ---")
    side_a = input("Введите сторону A: ")
    side_b = input("Введите сторону B: ")
    side_c = input("Введите сторону C: ")

    res_type, coords = calculate_triangle(side_a, side_b, side_c)

    print("\n--- Результат ---")
    print(f"Тип треугольника: '{res_type}'")
    print(f"Координаты вершин: {coords}")

if __name__ == "__main__":
    main()
