from __future__ import annotations

from dataclasses import asdict, is_dataclass
from config import METRIC_RANGES
from data.schema import Record


def validate_record(record: Record) -> tuple[bool, list[str]]:
    """
    Validates the current record before state detection.
    Verifies timestamp, numeric signals, and notes format.
    """
    errors: list[str] = []

    # Stop the flow early if the record is not a dataclass instance
    if not is_dataclass(record):
        return False, ["input must be a dataclass record"]

    # Convert the record into a dictionary for validation
    record_data = asdict(record)

    # Validate timestamp separately before saving to history
    timestamp = record_data.get("timestamp")
    if not isinstance(timestamp, str) or not timestamp.strip():
        errors.append("timestamp must be a non-empty string")

    # Review numeric signals using the configured ranges
    for field, (min_value, max_value) in METRIC_RANGES.items():
        value = record_data.get(field)

        if not isinstance(value, (int, float)):
            errors.append(f"{field} must be numeric")
            continue

        if not min_value <= value <= max_value:
            errors.append(
                f"{field} must be between {min_value} and {max_value}"
            )

    # Verify notes as text data
    notes = record_data.get("notes")
    if not isinstance(notes, str):
        errors.append("notes must be a string")

    return len(errors) == 0, errors
