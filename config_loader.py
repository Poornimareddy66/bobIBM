# config_loader.py
# Reads settings.cfg. Hand-rolled in 2013. Modernised 2024.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict:
    """Load key/value pairs from *path* (defaults to settings.cfg).

    Only keys listed in KNOWN_KEYS are retained; unknown keys are silently
    dropped (a typo in the file therefore never surfaces — known 2013 wart,
    kept for backward compatibility).
    """
    if path is None:
        path = SETTINGS_FILE
    settings: dict = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict, key: str, fallback: int) -> int:
    """Return *settings[key]* as an int, or *fallback* if absent or not parseable."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict, key: str, fallback: str = "") -> str:
    """Return *settings[key]* or *fallback* if the key is absent."""
    return settings.get(key, fallback)
