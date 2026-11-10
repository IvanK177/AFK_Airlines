
STATUS_ACTIVE = "оформлен"
STATUS_RETURNED = "возвращён"

from flights import free_seats


def next_order_id(orders):
    max_num = max((int(order["order_id"].split("-")[1]) for order in orders), default=0)
    return f"O-{max_num + 1:04d}"


def create_order(flights, orders, flight_code, customer, seats):
    flight = next((item for item in flights if item["code"] == flight_code), None)
    if flight is None:
        return False, f"Рейс с кодом '{flight_code}' не найден."
    if not isinstance(customer, str) or not customer.strip():
        return False, "Имя покупателя не может быть пустым."
    if type(seats) is not int or seats <= 0:
        return False, "Количество мест должно быть целым положительным числом больше нуля."
    available = free_seats(flight, orders)
    if seats > available:
        return False, f"Недостаточно свободных мест. Запрошено: {seats}, свободно: {available}."
    order_id = next_order_id(orders)
    orders.append({
        "order_id": order_id,
        "flight_code": flight_code,
        "customer": customer.strip(),
        "seats": seats,
        "status": STATUS_ACTIVE,
    })
    return True, f"Заказ {order_id} успешно оформлен."


def refund_order(orders, order_id):
    order = next((item for item in orders if item["order_id"] == order_id), None)
    if order is None:
        return False, f"Заказ с номером '{order_id}' не найден."
    if order["status"] == STATUS_RETURNED:
        return False, f"Заказ '{order_id}' уже был возвращён ранее."
    order["status"] = STATUS_RETURNED
    return True, f"Заказ {order_id} успешно возвращён."
