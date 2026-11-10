import pytest
from booking import next_order_id, create_order, refund_order, STATUS_ACTIVE, STATUS_RETURNED

@pytest.fixture
def mock_dataset():
    flights = [
        {"code": "SU1120", "origin": "Москва", "destination": "Сочи", "date": "2026-12-15", "capacity": 3}
    ]
    orders = [
        {"order_id": "O-0001", "flight_code": "SU1120", "customer": "Иванов Иван", "seats": 1, "status": STATUS_ACTIVE},
        {"order_id": "O-0002", "flight_code": "SU1120", "customer": "Петров Петр", "seats": 1, "status": STATUS_RETURNED}
    ]
    return flights, orders

def test_next_order_id_generation(mock_dataset):
    flights, orders = mock_dataset
    assert next_order_id(orders) == "O-0003"
    assert next_order_id([]) == "O-0001"

def test_create_order_success(mock_dataset):
    flights, orders = mock_dataset
    ok, msg = create_order(flights, orders, "SU1120", "Сидоров С.", 2)
    assert ok == True
    assert "O-0003" in msg
    assert len(orders) == 3
    assert orders[2]["status"] == STATUS_ACTIVE

def test_create_order_exceed_capacity(mock_dataset):
    flights, orders = mock_dataset
    ok, msg = create_order(flights, orders, "SU1120", "Сидоров С.", 3)
    assert ok == False
    assert "Недостаточно свободных мест" in msg
    assert len(orders) == 2

def test_create_order_empty_customer(mock_dataset):
    flights, orders = mock_dataset
    ok, msg = create_order(flights, orders, "SU1120", "   ", 1)
    assert ok == False
    assert "не может быть пустым" in msg

def test_create_order_invalid_seats(mock_dataset):
    flights, orders = mock_dataset
    ok1, msg1 = create_order(flights, orders, "SU1120", "Иван", 0)
    assert ok1 == False
    ok2, msg2 = create_order(flights, orders, "SU1120", "Иван", -1)
    assert ok2 == False
    ok3, msg3 = create_order(flights, orders, "SU1120", "Иван", True)
    assert ok3 == False

def test_refund_order_success(mock_dataset):
    flights, orders = mock_dataset
    ok, msg = refund_order(orders, "O-0001")
    assert ok == True
    assert orders[0]["status"] == STATUS_RETURNED

def test_refund_order_already_returned(mock_dataset):
    flights, orders = mock_dataset
    ok, msg = refund_order(orders, "O-0002")
    assert ok == False
    assert "уже был возвращён" in msg

def test_refund_order_nonexistent(mock_dataset):
    flights, orders = mock_dataset
    ok, msg = refund_order(orders, "O-9999")
    assert ok == False
    assert "не найден" in msg