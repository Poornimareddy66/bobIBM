# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_does_not_crash_when_last_service_km_missing():
    # A car without a 'last_service_km' entry (like VOS-7788 in fleet_sample.json)
    # must not raise a KeyError and must not be reported as due for service —
    # the absence of a reading means we treat the car as freshly serviced (0 % worn).
    fleet_with_missing = SAMPLE + [{"id": "VOS-7788", "odometer": 92000}]
    result = fleet_summary(fleet_with_missing)
    assert result["count"] == 3
    assert result["due"] == 1   # VOS-7788 has no reading → freshly serviced → not due
