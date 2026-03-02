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


# CLI diagnostics
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
    Prompts for text input.
    Cuts extra characters if too long.
    """
    txt = input(prompt).strip()

    # Limit text lengh
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
    4. Save to storage
    5. Detect current state
    """
    log.info("NEFILIM CLI - Nuevo registro")

    # Collect user inputs
    sleep_hours = _ask_float("Horas de sueño (0-16): ", 0, 16)
    mood = _ask_float("Ánimo (0-10): ", 0, 10)
    anxiety = _ask_float("Ansiedad (0-10): ", 0, 10)
    energy = _ask_float("Energía (0-10): ", 0, 10)
    focus = _ask_float("Enfoque (0-10): ", 0, 10)
    notes = _ask_text("Notas (opcional, max 500 chars): ")

    # Construct record object
    checkin = CheckIn(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        sleep_hours=sleep_hours,
        mood=mood,
        anxiety=anxiety,
        energy=energy,
        focus=focus,
        notes=notes,
    )

    # Validate user input
    ok, errors = validate_checkin(checkin)
    if not ok:
        log.info("Entrada inválido. Errores:")
        for e in errors:
            print(f"- {e}")
        return

    # Update stored history
    history = load_checkins(DEFAULT_STORAGE_PATH)
    history.append(checkin)
    save_checkins(DEFAULT_STORAGE_PATH, history)

    # Detect current state
    state, details = detect_state(checkin)

    log.info(f"Estado detectado: {state}")

    # Print details (if any)
    if details:
        print(details)


if __name__ == "__main__":
    # Run CLI when executed directly
    run()