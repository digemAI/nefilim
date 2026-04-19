from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


# Required fields for a valid NEFILIM record
REQUIRED_FIELDS = [
    "timestamp",
    "sleep_hours",
    "mood",
    "anxiety",
    "energy",
    "focus",
    "notes",
]


@dataclass(frozen=True)
class Record:
    """
    Represents one NEFILIM record.    
    """
    timestamp: str
    sleep_hours: float
    mood: float
    anxiety: float
    energy: float
    focus: float
    notes: str


@dataclass(frozen=True)
class AnalysisResult:
    """
    Output of state and trend analysis.    
    """
    state: str
    reason: str
    trend: str
    trend_reason: str
    recommendation: str
    recent_records_used: int


def build_record(
    sleep_hours: float,
    mood: float,
    anxiety: float,
    energy: float,
    focus: float,
    notes: str,
) -> Record:
    """
    Builds a record from the current input
    Adds a timestamp for the current session.
    """
    return Record(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        sleep_hours=sleep_hours,
        mood=mood,
        anxiety=anxiety,
        energy=energy,
        focus=focus,
        notes=notes,
    )


def record_from_dict(data: dict[str, Any]) -> Record | None:
    """
    Converts a dictionary into a Record.
    Returns None if the data is invalid.
    """
    try:
        # Convert raw data into a Record
        return Record(
            timestamp=str(data["timestamp"]),
            sleep_hours=float(data["sleep_hours"]),
            mood=float(data["mood"]),
            anxiety=float(data["anxiety"]),
            energy=float(data["energy"]),
            focus=float(data["focus"]),
            notes=str(data.get("notes", "")),
        )
    except (KeyError, TypeError, ValueError):
        # Ignore invalid or corrupted data
        return None