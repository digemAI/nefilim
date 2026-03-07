from __future__ import annotations
from dataclasses import asdict
from typing import Tuple, List, Any


def _is_number(x: Any) -> bool:
    """
    Returns True only for int/float values (not bool).
    """
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate_record(record) -> Tuple[bool, List[str]]:
    """
    Validates an input record.

    Ensures:
    - Required fields
    - Numeric values
    - Allowed ranges
    - Notes length

    Returns:
        (is_valid, errors)
    """
    errors: List[str] = []

    # Convert dataclass to dict for validation
    try:
        data = asdict(record)
    except Exception:
        return False, ["input must be a dataclass instance"]

    # Validate required fields
    required = ["timestamp", "sleep_hours", "mood", "anxiety", "energy", "focus", "notes"]
    for k in required:
        if k not in data:
            errors.append(f"missing field: {k}")

    # Validate emotional metrics (0–10 scale)
    for k in ["mood", "anxiety", "energy", "focus"]:
        if k in data:
            if not _is_number(data[k]):
                errors.append(f"{k} must be a number (0-10)")
            elif not (0 <= data[k] <= 10):
                errors.append(f"{k} out of range (0-10)")

    # Validate sleep hours within realistic limits
    if "sleep_hours" in data:
        if not _is_number(data["sleep_hours"]):
            errors.append("sleep_hours must be a number")
        elif not (0 <= data["sleep_hours"] <= 16):
            errors.append("sleep_hours out of range (0-16)")

    # Validate notes length
    if "notes" in data and isinstance(data["notes"], str):
        if len(data["notes"]) > 500:
            errors.append("notes too long (max 500 chars)")

    return (len(errors) == 0), errors
