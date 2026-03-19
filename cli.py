from __future__ import annotations

from core.logger import build_logger
from core.state_detector import detect_state
from core.validator import validate_record
from data.schema import build_record
from data.storage import append_history

log = build_logger()


def prompt_float(message: str) -> float:
    """
    Keeps asking until a valid number is entered.
    """
    while True:
        raw_value = input(message).strip()

        try:
            return float(raw_value)
        except ValueError:
            print("Enter a valid number.")


def prompt_text(message: str, max_len: int = 500) -> str:
    """
    Collects text input and shortens it if needed.
    """
    text = input(message).strip()
    return text[:max_len]


def run_cli() -> None:
    """
    Runs the main NEFILIM CLI flow
    Shows the detected state and saved path.
    """
    log.info("NEFILIM CLI - New record")

    # Collect the current user signals
    sleep_hours = prompt_float("Sleep hours (0-24): ")
    mood = prompt_float("Mood (0-10): ")
    anxiety = prompt_float("Anxiety (0-10): ")
    energy = prompt_float("Energy (0-10): ")
    focus = prompt_float("Focus (0-10): ")
    notes = prompt_text("Notes (optional, max 500 characters): ")

    # Gather the current input from the usert
    record = build_record(
        sleep_hours=sleep_hours,
        mood=mood,
        anxiety=anxiety,
        energy=energy,
        focus=focus,
        notes=notes,
    )

    # Stop the CLI flow if the record is invalid
    is_valid, errors = validate_record(record)
    if not is_valid:
        log.warning("Invalid input detected during CLI validation.")
        print("\nValidation errors:")
        for error in errors:
            print(f"- {error}")
        return

    # Detect the current state from the validated record
    result = detect_state(record)

    # Save the validated record to history
    saved_path = append_history(record)

    log.info(f"Detected state: {result.state} | reason: {result.reason}")

    print("\n--- Result ---")
    print(f"State: {result.state}")
    print(f"Reason: {result.reason}")
    print(f"Saved to: {saved_path}")