import sys
from booking import create_order, refund_order
from flights import free_seats, search_flights
from orders import filter_orders, print_orders, MOCK_ORDERS

def main():
    settings = {
        "flights_file": "data/flights.csv",
        "orders_file": "data/orders.csv",
        "report_file": "data/report.xlsx",
        "log_file": "data/app.log"
    }
    
    flights = [
        {"code": "SU1120", "origin": "Москва", "destination": "Сочи", "date": "2026-12-15", "capacity": "3"},
        {"code": "S72504", "origin": "Москва", "destination": "Новосибирск", "date": "2026-12-20", "capacity": "150"}
    ]
    orders = [order.copy() for order in MOCK_ORDERS]

    while True:
        print("=== СИСТЕМА БРОНИРОВАНИЯ АВИАБИЛЕТОВ ===")
        print("1. Поиск рейсов")
        print("2. Оформление заказа")
        print("3. Просмотр истории заказов")
        print("4. Возврат билета")
        print("5. Выход")
        
        choice = input("Выберите пункт меню (1-5): ").strip()
        
        if not choice:
            print("\n[Ошибка] Вы ничего не ввели. Попробуйте снова.\n")
            continue
            
        if choice == "1":
            origin = input("Город отправления: ")
            destination = input("Город назначения: ")
            date = input("Дата (ГГГГ-ММ-ДД): ")
            found_flights = search_flights(flights, origin, destination, date)
            if not found_flights:
                print("\nРейсы не найдены.\n")
            else:
                for flight in found_flights:
                    print(
                        f"\n{flight['code']}: {flight['origin']} -> "
                        f"{flight['destination']}, {flight['date']}, "
                        f"свободно мест: {free_seats(flight, orders)}\n"
                    )
            
        elif choice == "2":
            flight_code = input("Код рейса: ").strip()
            customer = input("Имя покупателя: ")
            seats_input = input("Количество мест: ")
            try:
                seats = int(seats_input)
            except ValueError:
                print("\n[Ошибка] Количество мест должно быть целым числом.\n")
                continue
            success, message = create_order(
                flights, orders, flight_code, customer, seats
            )
            print(f"\n{message}\n")
            
        elif choice == "3":
            print("\n--- Настройки фильтрации (Оставьте пустым для пропуска) ---")
            filter_flight = input("Фильтр по коду рейса: ").strip()
            filter_status = input("Фильтр по статусу (оформлен/возвращён): ").strip()
            
            current_orders = filter_orders(orders, filter_flight, filter_status)
            print_orders(current_orders)
            
        elif choice == "4":
            order_id = input("Номер заказа: ").strip()
            success, message = refund_order(orders, order_id)
            print(f"\n{message}\n")
            
        elif choice == "5":
            print("\nРабота завершена. До свидания!")
            sys.exit(0)
            
        else:
            print(f"\n[Ошибка] Команды '{choice}' не существует. Введите число от 1 до 5.\n")

if __name__ == "__main__":
    main()
