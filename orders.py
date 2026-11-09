STATUS_ACTIVE = "оформлен"
STATUS_RETURNED = "возвращён"

# данные для тестов 
MOCK_ORDERS = [
    {"order_id": "O-0001", "flight_code": "SU1120", "customer": "Иванов Иван", "seats": "2", "status": "оформлен"},
    {"order_id": "O-0002", "flight_code": "SU1120", "customer": "Петров Петр", "seats": "1", "status": "возвращён"},
    {"order_id": "O-0003", "flight_code": "S72504", "customer": "Сидоров Сидор", "seats": "3", "status": "оформлен"},
]

def filter_orders(orders, flight_code, status):
    """Фильтрует список заказов. Пустая строка означает 'любое значение'."""
    filtered = []
    for order in orders:
        match_flight = (flight_code == "" or order["flight_code"] == flight_code)
        match_status = (status == "" or order["status"] == status)
        if match_flight and match_status:
            filtered.append(order)
    return filtered

def print_orders(orders):
    """Выводит историю заказов в красивом табличном виде."""
    if not orders:
        print("\nЗаказы не найдены.")
        return

   
    print("\n" + "=" * 80)
    print(f"{'ID Заказа':<10} | {'Рейс':<10} | {'Пассажир':<25} | {'Места':<8} | {'Статус':<12}")
    print("-" * 80)
    
    for order in orders:

        seats_count = int(order["seats"])
        print(f"{order['order_id']:<10} | {order['flight_code']:<10} | {order['customer']:<25} | {seats_count:<8} | {order['status']:<12}")
    print("=" * 80 + "\n")
