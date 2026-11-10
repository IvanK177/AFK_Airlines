
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


def search_flights(flights, origin, destination, date):
    origin = origin.strip().lower()
    destination = destination.strip().lower()
    date = date.strip()
    return [
        flight
        for flight in flights
        if flight["origin"].strip().lower() == origin
        and flight["destination"].strip().lower() == destination
        and flight["date"].strip() == date
    ]
