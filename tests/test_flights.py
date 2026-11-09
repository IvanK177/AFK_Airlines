import os
import pytest
from flights import search_flights, free_seats, validate_flights_csv, STATUS_ACTIVE, STATUS_RETURNED


def get_sample_flights():
    return [
        {"code": "SU1120", "origin": "Москва", "destination": "Сочи", "date": "2026-12-15", "capacity": 3},
        {"code": "DP201", "origin": "Москва", "destination": "Санкт-Петербург", "date": "2026-12-15", "capacity": 100},
        {"code": "S71050", "origin": "Новосибирск", "destination": "Москва", "date": "2026-12-20", "capacity": 150},
    ]


def test_search_flights_case_insensitive_and_spaces():
    flights = get_sample_flights()
    found = search_flights(flights, "  мОсКвА  ", "  сочи  ", " 2026-12-15 ")

    assert len(found) == 1
    assert found[0]["code"] == "SU1120"


def test_search_flights_not_found():
    flights = get_sample_flights()
    found = search_flights(flights, "Самара", "Казань", "2026-12-15")
    assert found == []


def test_free_seats_calculation():
    flight = {"code": "SU1120", "origin": "Москва", "destination": "Сочи", "date": "2026-12-15", "capacity": 3}

    orders = [
        {"order_id": "O-0001", "flight_code": "SU1120", "customer": "Иванов", "seats": 2, "status": STATUS_ACTIVE},
        {"order_id": "O-0002", "flight_code": "SU1120", "customer": "Петров", "seats": 1, "status": STATUS_RETURNED},
        {"order_id": "O-0003", "flight_code": "DP201", "customer": "Сидоров", "seats": 5, "status": STATUS_ACTIVE},
    ]

    available = free_seats(flight, orders)
    assert available == 1


def test_free_seats_zero_remaining():
    flight = {"code": "SU1120", "origin": "Москва", "destination": "Сочи", "date": "2026-12-15", "capacity": 3}

    orders = [
        {"order_id": "O-0001", "flight_code": "SU1120", "customer": "Иванов", "seats": 3, "status": STATUS_ACTIVE}
    ]

    assert free_seats(flight, orders) == 0


def test_validate_flights_csv_valid_file():
    valid_csv_path = os.path.join("data", "flights.csv")
    rows, errors = validate_flights_csv(valid_csv_path)

    assert errors == []
    assert len(rows) == 4
    assert rows[0]["code"] == "SU1120"
    assert rows[0]["capacity"] == 3


def test_validate_flights_csv_invalid_file():
    invalid_csv_path = os.path.join("data", "invalid_flights.csv")
    rows, errors = validate_flights_csv(invalid_csv_path)

    assert rows == []
    assert len(errors) >= 3

    errors_text = "\n".join(errors)
    assert "Строка 2" in errors_text
    assert "Строка 3" in errors_text
    assert "Строка 4" in errors_text


def test_validate_flights_csv_existing_code(tmp_path):
    csv_file = tmp_path / "temp_flights.csv"
    csv_file.write_text(
        "code,origin,destination,date,capacity\n"
        "EXISTING01,Москва,Казань,2026-12-15,100\n",
        encoding="utf-8"
    )

    existing_codes = ["EXISTING01"]
    rows, errors = validate_flights_csv(str(csv_file), existing_codes=existing_codes)

    assert rows == []
    assert len(errors) == 1
    assert "уже существует" in errors[0]


def test_validate_flights_csv_bad_header(tmp_path):
    csv_file = tmp_path / "bad_header.csv"
    csv_file.write_text(
        "id,from_city,to_city,fly_date,places\n"
        "SU100,Москва,Сочи,2026-12-15,100\n",
        encoding="utf-8"
    )

    rows, errors = validate_flights_csv(str(csv_file))

    assert rows == []
    assert len(errors) == 1
    assert "Неверный заголовок" in errors[0]
