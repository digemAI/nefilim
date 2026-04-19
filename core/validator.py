from __future__ import annotations

from dataclasses import asdict, is_dataclass

from config import METRIC_RANGES
from data.schema import Record


def validate_record(record: Record) -> tuple[bool, list[str]]:
    """
    Validates a record before state detection.
    Checks timestamp, numeric signals, and notes.
    """
    errors: list[str] = []

    # Stop early if the input is not a dataclass record
    if not is_dataclass(record):
        return False, ["input must be a dataclass record"]

    record_data = asdict(record)

    # Check the timestamp field
    timestamp = record_data.get("timestamp")
    if not isinstance(timestamp, str) or not timestamp.strip():
        errors.append("timestamp must contain a valid text value")

    # Validate numeric signals using the configured ranges
    for field, (min_value, max_value) in METRIC_RANGES.items():
        value = record_data.get(field)

        if not isinstance(value, (int, float)):
            errors.append(f"{field} must be numeric")
            continue

        if not min_value <= value <= max_value:
            errors.append(f"{field} must be between {min_value} and {max_value}")

    # Check notes as plain text
    notes = record_data.get("notes")
    if not isinstance(notes, str):
        errors.append("notes must be a string")

    return len(errors) == 0, errors