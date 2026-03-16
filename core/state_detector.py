from __future__ import annotations

from dataclasses import dataclass

from data.schema import Record


@dataclass(frozen=True)
class StateResult:
    state: str
    reason: str


def detect_state(record: Record) -> StateResult:
    """
    Detects the current state from the input record.
    Returns the state together with the reason behind it.
    """
    sleep_hours = record.sleep_hours
    mood = record.mood
    anxiety = record.anxiety
    energy = record.energy
    focus = record.focus

    # Prioritize the highest-risk combinations first
    if anxiety >= 8 and focus <= 3:
        return StateResult("risk", "high anxiety with very low focus")

    if sleep_hours <= 4 and energy <= 3:
        return StateResult("risk", "very low sleep with very low energy")

    if mood <= 2 and anxiety >= 7:
        return StateResult("risk", "very low mood with high anxiety")

    # Review warning signals before returning a stable state
    if sleep_hours < 6:
        return StateResult("warning", "sleep slightly low")

    if anxiety >= 6:
        return StateResult("warning", "anxiety elevated")

    if energy <= 4:
        return StateResult("warning", "energy low")

    if focus <= 4:
        return StateResult("warning", "focus low")

    if mood <= 4:
        return StateResult("warning", "mood slightly low")

    return StateResult("stable", "metrics look stable")
