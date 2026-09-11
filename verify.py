"""verify.py — run this to confirm all tests pass without pytest.

Usage:
    python verify.py

It imports the production modules directly and runs every assertion.
Any failure will print the failing test name and the exception, then exit 1.
"""

import sys
import traceback


def run(name, fn):
    try:
        fn()
        print(f"  PASS  {name}")
    except Exception as exc:
        print(f"  FAIL  {name}")
        traceback.print_exc()
        sys.exit(1)


# ── km_wachter tests ─────────────────────────────────────────────────────────

from km_wachter import needs_service, wear_percent, SERVICE_INTERVAL_KM, WARN_AT_PERCENT


def t_almost_due_car_is_flagged():
    assert needs_service({"id": "VOS-4471", "odometer": 14900, "last_service_km": 0}) is True


def t_missing_reading_is_not_treated_as_zero():
    assert needs_service({"id": "VOS-7788", "odometer": 92000}) is False


# ── fleet_report tests ───────────────────────────────────────────────────────

from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def t_summary_counts_due_cars():
    assert fleet_summary(SAMPLE)["due"] == 1


def t_summary_does_not_crash_when_last_service_km_missing():
    fleet_with_missing = SAMPLE + [{"id": "VOS-7788", "odometer": 92000}]
    result = fleet_summary(fleet_with_missing)
    assert result["count"] == 3
    assert result["due"] == 1


# ── Constants sanity-check ───────────────────────────────────────────────────

def t_constants_unchanged():
    assert SERVICE_INTERVAL_KM == 15000, "Service interval must stay at 15 000 km"
    assert WARN_AT_PERCENT == 80, "Warn threshold must stay at 80 %"


# ── fleet_utils sanity-check ─────────────────────────────────────────────────

from fleet_utils import km_to_miles, KM_TO_MILES


def t_km_to_miles_direction():
    # 100 km → ~62.1 miles, not 160.9 miles
    result = km_to_miles(100)
    assert 60 < result < 65, f"km_to_miles(100) = {result}, expected ~62.1"


# ── wear_percent boundary checks ─────────────────────────────────────────────

def t_wear_percent_float_division():
    # 14 900 of 15 000 km used → ~99.3 %, must be above 80
    pct = wear_percent(14900, 15000)
    assert pct > 80, f"wear_percent(14900,15000) = {pct}, expected >80"


def t_wear_percent_just_below_threshold():
    # 11 999 of 15 000 km → ~79.99 %, must be below 80
    pct = wear_percent(11999, 15000)
    assert pct < 80, f"wear_percent(11999,15000) = {pct}, expected <80"


if __name__ == "__main__":
    print("Running tests …\n")
    run("test_almost_due_car_is_flagged", t_almost_due_car_is_flagged)
    run("test_missing_reading_is_not_treated_as_zero", t_missing_reading_is_not_treated_as_zero)
    run("test_summary_counts_due_cars", t_summary_counts_due_cars)
    run("test_summary_does_not_crash_when_last_service_km_missing",
        t_summary_does_not_crash_when_last_service_km_missing)
    run("test_constants_unchanged", t_constants_unchanged)
    run("test_km_to_miles_direction", t_km_to_miles_direction)
    run("test_wear_percent_float_division", t_wear_percent_float_division)
    run("test_wear_percent_just_below_threshold", t_wear_percent_just_below_threshold)
    print("\nAll tests passed.")
