from __future__ import annotations
from datetime import datetime
from dataclasses import asdict

# Configuration and core modules
from config import HISTORY_FILE_PATH
from core.logger import build_logger
from core.state_detector import detect_state
from core.validator import validate_record

# Data layer
from data.schema import Record
from data.storage import append_history

log = build_logger()


def _ask_float(
    prompt: str,
    min_v: float | None = None,
    max_v: float | None = None
) -> float:
    """
    Prompts until a valid float is entered.
    Applies optional min/max bounds.
    """
    while True:
        raw = input(prompt).strip()

        try:
            v = float(raw)
        except ValueError:
            print("Enter a valid number.")
            continue

        # Lower bound validation
        if min_v is not None and v < min_v:
            print(f"Value must be >= {min_v}")
            continue

        # Upper bound validation
        if max_v is not None and v > max_v:
            print(f"Value must be <= {max_v}")
            continue

        return v


def _ask_text(prompt: str, max_len: int = 500) -> str:
    """
    Prompts for text input.
    Cuts extra characters if too long.
    """
    txt = input(prompt).strip()

    if len(txt) > max_len:
        txt = txt[:max_len]

    return txt


def run() -> None:
    """
    CLI entry point.

    flow:
    1. Collect user input
    2. Create record
    3. Validate input
    4. Detect current state
    5. Save to storage
    """
    log.info("NEFILIM CLI - New record")

    # Collect user inputs
    sleep_hours = _ask_float("Sleep hours (0-16): ", 0, 16)
    mood        = _ask_float("Mood (0-10): ", 0, 10)
    anxiety     = _ask_float("Anxiety (0-10): ", 0, 10)
    energy      = _ask_float("Energy (0-10): ", 0, 10)
    focus       = _ask_float("Focus (0-10): ", 0, 10)
    notes       = _ask_text("Notes (optional, max 500 characters): ")

    # Construct record object
    record = Record(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        sleep_hours=sleep_hours,
        mood=mood,
        anxiety=anxiety,
        energy=energy,
        focus=focus,
        notes=notes,
    )

    # Validate user input
    ok, errors = validate_record(record)
    if not ok:
        log.info("Invalid input. Errors:")
        for e in errors:
            print(f"  - {e}")
        return

    # Detect current state
    result = detect_state(
        sleep_hours=sleep_hours,
        stress=0,       # stress not collected in CLI yet; default 0
        anxiety=int(anxiety),
    )

    log.info(f"Detected state: {result.state} — {result.reason}")

    # Save record to history (convert dataclass to dict first)
    append_history(HISTORY_FILE_PATH, asdict(record))


if __name__ == "__main__":
    run()
