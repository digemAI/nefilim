from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


# Fields required to build a valid NEFILIM record
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
    timestamp: str
    sleep_hours: float
    mood: float
    anxiety: float
    energy: float
    focus: float
    notes: str


def build_record(
    sleep_hours: float,
    mood: float,
    anxiety: float,
    energy: float,
    focus: float,
    notes: str,
) -> Record:
    """
    Builds the current record from CLI input.
    Adds a timestamp before storing it in history.
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
