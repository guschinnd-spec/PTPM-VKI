
def calculate_discount(price: float, customer_type: str, has_promo: bool) -> float:
    if price < 0:
        raise ValueError("Цена не может быть отрицательной")
    discount = 0.0
    if customer_type == "vip":
        discount = 0.20
    elif customer_type == "regular":
        discount = 0.05
    if has_promo:
        discount += 0.10
    if discount > 0.30:
        discount = 0.30
    return round(price * (1 - discount), 2)