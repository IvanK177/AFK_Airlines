STATUS_ACTIVE = "оформлен"
STATUS_RETURNED = "возвращён"

from flights import free_seats

def next_order_id(orders):
    max_num = 0
    for o in orders:
        oid = o["order_id"]
        parts = oid.split("-")
        num = int(parts[1])
        if num > max_num:
            max_num = num
    new_num = max_num + 1
    return "O-" + str(new_num).zfill(4)

def create_order(flights, orders, flight_code, customer, seats):
    found_flight = None
    for f in flights:
        if f["code"] == flight_code:
            found_flight = f
            break

    if found_flight is None:
        return False, "Рейс с кодом '" + str(flight_code) + "' не найден."

    if not isinstance(customer, str) or customer.strip() == "":
        return False, "Имя покупателя не может быть пустым."

    if type(seats) != int or seats <= 0:
        return False, "Количество мест должно быть целым положительным числом больше нуля."

    free = free_seats(found_flight, orders)
    if seats > free:
        return False, "Недостаточно свободных мест. Запрошено: " + str(seats) + ", свободно: " + str(free) + "."

    order_id = next_order_id(orders)
    new_order = {
        "order_id": order_id,
        "flight_code": flight_code,
        "customer": customer.strip(),
        "seats": seats,
        "status": STATUS_ACTIVE
    }
    orders.append(new_order)
    return True, "Заказ " + order_id + " успешно оформлен."

def refund_order(orders, order_id):
    found_order = None
    for o in orders:
        if o["order_id"] == order_id:
            found_order = o
            break

    if found_order is None:
        return False, "Заказ с номером '" + str(order_id) + "' не найден."

    if found_order["status"] == STATUS_RETURNED:
        return False, "Заказ '" + str(order_id) + "' уже был возвращён ранее."

    found_order["status"] = STATUS_RETURNED
    return True, "Заказ " + str(order_id) + " успешно возвращён."