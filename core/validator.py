from __future__ import annotations
from dataclasses import asdict
from typing import Tuple, List, Any


def _is_number(x: Any) -> bool:
    """
    Returns True only for int/float values (explicitly excluding bool).
    """
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate_checkin(checkin_obj) -> Tuple[bool, List[str]]:
    """
    Validates a CheckIn dataclass instance.

    Performs:
    - Structural validation (required fields)
    - Type validation (numeric fields)
    - Range validation (bounded scales)
    - Text length constraint

    Returns:
        (is_valid, list_of_errors)
    """
    errors: List[str] = []

    # Convert dataclass to dictionary for easier field inspection
    try:
        data = asdict(checkin_obj)
    except Exception:
        return False, ["checkin must be a dataclass instance"]

    # Required fields validation
    required = ["timestamp", "sleep_hours", "mood", "anxiety", "energy", "focus", "notes"]
    for k in required:
        if k not in data:
            errors.append(f"missing field: {k}")

    # Numeric scale validation (0–10 emotional metrics)
    for k in ["mood", "anxiety", "energy", "focus"]:
        if k in data:
            if not _is_number(data[k]):
                errors.append(f"{k} must be a number (0-10)")
            elif not (0 <= data[k] <= 10):
                errors.append(f"{k} out of range (0-10)")

    # Sleep hours sanity check (physiological bounds) 
    if "sleep_hours" in data:
        if not _is_number(data["sleep_hours"]):
            errors.append("sleep_hours must be a number")
        elif not (0 <= data["sleep_hours"] <= 16):
            errors.append("sleep_hours out of range (0-16)")

    # Notes length guard (prevent oversized entries)
    if "notes" in data and isinstance(data["notes"], str):
        if len(data["notes"]) > 500:
            errors.append("notes too long (max 500 chars)")

    return (len(errors) == 0), errors