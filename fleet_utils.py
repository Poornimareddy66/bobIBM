# fleet_utils.py
# Catch-all helpers since 2013. Modernised 2024.

# Correct factor: 1 km = 0.621371 miles.
# The original value (1.609) was the km-per-mile constant used in the wrong direction,
# so every reported mileage was ~2.6× too large.
KM_TO_MILES = 0.621371


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km * KM_TO_MILES


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a number as a whole-number percentage string."""
    return f"{value:.0f}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of *values*, or 0 for an empty list."""
    total = 0.0
    count = 0
    for v in values:
        total += v
        count += 1
    if count == 0:
        return 0.0
    return total / count


def is_due(pct: float, threshold: float) -> bool:
    """Return True when *pct* meets or exceeds *threshold*."""
    return pct >= threshold


def parse_service_date(text: str) -> tuple[int, int, int] | None:
    """Parse a DD.MM.YYYY date string into a (year, month, day) tuple.

    Returns None if the format does not match.
    """
    parts = text.split(".")
    if len(parts) != 3:
        return None
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    return (year, month, day)


def chunk_list(items: list, size: int) -> list[list]:
    """Split *items* into consecutive chunks of *size*.

    The final chunk may be smaller than *size*.
    """
    chunks = []
    current: list = []
    for item in items:
        current.append(item)
        if len(current) == size:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks
