# log_util.py
# A homemade logger. Modernised 2024.

import time

LOG_LINES: list[str] = []   # global state, shared by everyone who imports this
DEBUG = False


def log(message: str) -> None:
    """Append a timestamped *message* to the in-memory log and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log *message* at DEBUG level (no-op unless DEBUG is True)."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Write buffered log lines to *path* (append mode) then clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
