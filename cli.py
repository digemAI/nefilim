from __future__ import annotations

from core.logger import build_logger
from core.state_detector import analyze_state
from core.validator import validate_record
from data.schema import build_record
from data.storage import append_history, load_record_history

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
    Runs the main NEFILIM CLI flow.
    Detects the current state and reviews recent history.
    """
    log.info("NEFILIM CLI - New record")

    # Collect the current input from the user
    sleep_hours = prompt_float("Sleep hours (0-24): ")
    mood = prompt_float("Mood (0-10): ")
    anxiety = prompt_float("Anxiety (0-10): ")
    energy = prompt_float("Energy (0-10): ")
    focus = prompt_float("Focus (0-10): ")
    notes = prompt_text("Notes (optional, max 500 characters): ")

    # Build the record for validation and analysis
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

    # Run state detection and history analysis
    history = load_record_history()
    analysis = analyze_state(record, history)

    # Save the current record to history storage
    saved_path = append_history(record)

    log.info(
        "Detected state: %s | reason: %s | trend: %s | trend_reason: %s",
        analysis.state,
        analysis.reason,
        analysis.trend,
        analysis.trend_reason,
    )

    # Show the final analysis result to the user
    formatted_trend = analysis.trend.replace("_", " ")

    print("\n--- Result ---")
    print(f"State: {analysis.state}")
    print(f"Reason: {analysis.reason}")
    print(f"Trend: {formatted_trend}")
    print(f"Trend reason: {analysis.trend_reason}")
    print(f"Recommendation: {analysis.recommendation}")
    print(f"Recent records used: {analysis.recent_records_used}")
    print(f"Saved to: {saved_path}")