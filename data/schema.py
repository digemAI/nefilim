from dataclasses import dataclass

# Record structure
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
