import sys
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
    orders = MOCK_ORDERS

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
            print("\n[Заглушка] Поиск рейсов (вызов search_flights)...\n")
            
        elif choice == "2":
            print("\n[Заглушка] Оформление заказа (вызов create_order)...\n")
            
        elif choice == "3":
            print("\n--- Настройки фильтрации (Оставьте пустым для пропуска) ---")
            filter_flight = input("Фильтр по коду рейса: ").strip()
            filter_status = input("Фильтр по статусу (оформлен/возвращён): ").strip()
            
            current_orders = filter_orders(orders, filter_flight, filter_status)
            print_orders(current_orders)
            
        elif choice == "4":
            print("\n[Заглушка] Возврат билета (вызов refund_order)...\n")
            
        elif choice == "5":
            print("\nРабота завершена. До свидания!")
            sys.exit(0)
            
        else:
            print(f"\n[Ошибка] Команды '{choice}' не существует. Введите число от 1 до 5.\n")

if __name__ == "__main__":
    main()
