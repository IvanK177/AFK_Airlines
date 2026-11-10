
STATUS_ACTIVE = "оформлен"


def free_seats(flight, orders):
    capacity = int(flight["capacity"])
    taken = sum(
        int(order["seats"])
        for order in orders
        if order["flight_code"] == flight["code"]
        and order["status"] == STATUS_ACTIVE
    )
    return capacity - taken
