# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Modernised 2024.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return the percentage of the service interval consumed.

    Uses float division so a car at 14 900 km of a 15 000 km window
    correctly reports ~99 %, not 0 %.
    """
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True when the car has consumed WARN_AT_PERCENT of its service window.

    If 'last_service_km' is absent the car is treated as freshly serviced
    (i.e. last service happened at the current odometer reading), so a missing
    entry never triggers a false alarm.
    """
    odometer = car["odometer"]
    last = car.get("last_service_km", odometer)   # absent → freshly serviced
    km_since = odometer - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list:
    """Flag every car that is due for service and print its ID.

    Returns the list of flagged car IDs.
    """
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
