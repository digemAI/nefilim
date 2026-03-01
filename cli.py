from __future__ import annotations
from datetime import datetime

# Configuration and core modules
from config import DEFAULT_STORAGE_PATH
from core.logger import build_logger
from core.state_detector import detect_state
from core.validator import validate_checkin

# Data layer
from data.schema import CheckIn
from data.storage import load_checkins, save_checkins


# Logger used in this CLI

def _ask_float(
    prompt: str,
    min_v: float | None = None,
    max_v: float | None = None
) -> float:
    """
    Keeps asking for a number until the user enters a valid one.
    Respects min/max limits if they are defined.
    """
    while True:
        raw = input(prompt).strip()

        try:
            v = float(raw)
        except ValueError:
            print("Pon un número válido.")
            continue

        # Lower bound validation
        if min_v is not None and v < min_v:
            print(f"Debe ser >= {min_v}")
            continue

        # Upper bound validation
        if max_v is not None and v > max_v:
            print(f"Debe ser <= {max_v}")
            continue

        return v


def _ask_text(prompt: str, max_len: int = 500) -> str:
    """
    Prompts the user for free text input.
    Truncates input if it exceeds max_len.
    """
    txt = input(prompt).strip()

    # Prevent oversized entries
    if len(txt) > max_len:
        txt = txt[:max_len]

    return txt


def run() -> None:
    """
    Main CLI entry point.

    Workflow:
    1. Collect user input
    2. Build CheckIn object
    3. Validate input
    4. Persist to storage
    5. Detect psychological state
    """
    log.info("NEFILIM CLI - Nuevo check-in")

    # ---- Collect user metrics ----
    sleep_hours = _ask_float("Horas de sueño (0-16): ", 0, 16)
    mood = _ask_float("Ánimo (0-10): ", 0, 10)
    anxiety = _ask_float("Ansiedad (0-10): ", 0, 10)
    energy = _ask_float("Energía (0-10): ", 0, 10)
    focus = _ask_float("Enfoque (0-10): ", 0, 10)
    notes = _ask_text("Notas (opcional, max 500 chars): ")

    # ---- Construct domain object ----
    checkin = CheckIn(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        sleep_hours=sleep_hours,
        mood=mood,
        anxiety=anxiety,
        energy=energy,
        focus=focus,
        notes=notes,
    )

    # ---- Validation layer ----
    ok, errors = validate_checkin(checkin)
    if not ok:
        log.info("Check-in inválido. Errores:")
        for e in errors:
            print(f"- {e}")
        return

    # ---- Persistence layer ----
    history = load_checkins(DEFAULT_STORAGE_PATH)
    history.append(checkin)
    save_checkins(DEFAULT_STORAGE_PATH, history)

    # ---- State detection (core logic) ----
    state, details = detect_state(checkin)

    log.info(f"Estado detectado: {state}")

    # Optional explanation from detector
    if details:
        print(details)


if __name__ == "__main__":
    # Execute CLI only when run directly
    run()