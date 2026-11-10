import csv
from datetime import datetime

STATUS_ACTIVE = "оформлен"
STATUS_RETURNED = "возвращён"
FLIGHT_COLUMNS = ["code", "origin", "destination", "date", "capacity"]
DATE_FORMAT = "%Y-%m-%d"


def free_seats(flight, orders):
    capacity = int(flight["capacity"])
    taken = 0
    for o in orders:
        if o["flight_code"] == flight["code"] and o["status"] == STATUS_ACTIVE:
            taken += int(o["seats"])
    return capacity - taken


def search_flights(flights, origin, destination, date):
    result = []
    origin = origin.strip().lower()
    destination = destination.strip().lower()
    date = date.strip()

    for f in flights:
        if f["origin"].strip().lower() == origin and f["destination"].strip().lower() == destination and f["date"].strip() == date:
            result.append(f)
    return result


def validate_flights_csv(path, existing_codes=None):
    if existing_codes is None:
        existing_codes = []

    errors = []
    rows = []
    seen = []

    with open(path, "r", encoding="utf-8-sig") as f:
        lines = list(csv.reader(f))

    if len(lines) == 0:
        return [], ["Файл пуст"]

    if lines[0] != FLIGHT_COLUMNS:
        return [], ["Неверный заголовок файла"]

    line_num = 1
    for row in lines[1:]:
        line_num += 1

        if len(row) != 5:
            errors.append(f"Строка {line_num}: неверное количество колонок")
            continue

        code, origin, destination, date_str, cap_str = row
        code = code.strip()
        origin = origin.strip()
        destination = destination.strip()
        date_str = date_str.strip()
        cap_str = cap_str.strip()

        if not code:
            errors.append(f"Строка {line_num}: код рейса не может быть пустым")
        elif code in seen:
            errors.append(f"Строка {line_num}: дубликат кода рейса {code}")
        elif code in existing_codes:
            errors.append(f"Строка {line_num}: рейс с кодом {code} уже существует")
        else:
            seen.append(code)

        if not origin:
            errors.append(f"Строка {line_num}: пункт отправления не может быть пустым")

        if not destination:
            errors.append(f"Строка {line_num}: пункт назначения не может быть пустым")

        try:
            datetime.strptime(date_str, DATE_FORMAT)
        except ValueError:
            errors.append(f"Строка {line_num}: некорректная дата {date_str}")

        cap = 0
        try:
            cap = int(cap_str)
            if cap <= 0:
                errors.append(f"Строка {line_num}: вместимость должна быть больше 0")
        except ValueError:
            errors.append(f"Строка {line_num}: вместимость не число")

        rows.append({
            "code": code,
            "origin": origin,
            "destination": destination,
            "date": date_str,
            "capacity": cap
        })

    if len(errors) > 0:
        return [], errors

    return rows, []


def import_flights(path, flights):
    return False, "Not implemented yet"


def export_orders_xlsx(path, orders):
    return False, "Not implemented yet"
