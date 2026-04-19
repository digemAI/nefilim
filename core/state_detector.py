from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from config import (
    HIGH_RISK_RATIO,
    HIGH_WARNING_RATIO,
    IMPROVING_DELTA,
    RECENT_HISTORY_LIMIT,
    RISK_ANXIETY_THRESHOLD,
    RISK_ENERGY_THRESHOLD,
    RISK_FOCUS_THRESHOLD,
    RISK_MOOD_THRESHOLD,
    RISK_SLEEP_THRESHOLD,
    RISK_STREAK_LIMIT,
    TREND_WINDOW,
    WARNING_ANXIETY_THRESHOLD,
    WARNING_ENERGY_THRESHOLD,
    WARNING_FOCUS_THRESHOLD,
    WARNING_MOOD_THRESHOLD,
    WARNING_SLEEP_THRESHOLD,
    WARNING_STREAK_LIMIT,
    WORSENING_DELTA,
)
from data.schema import AnalysisResult, Record


@dataclass(frozen=True)
class StateResult:
    state: str
    reason: str


@dataclass(frozen=True)
class TrendResult:
    trend: str
    trend_reason: str
    recommendation: str
    recent_records_used: int


def detect_state(record: Record) -> StateResult:
    """
    Detects the current state from the input record.
    Returns the state and the main reason behind it.
    """
    sleep_hours = record.sleep_hours
    mood = record.mood
    anxiety = record.anxiety
    energy = record.energy
    focus = record.focus

    # Prioritize high-risk combinations first
    if anxiety >= RISK_ANXIETY_THRESHOLD and focus <= RISK_FOCUS_THRESHOLD:
        return StateResult("risk", "high anxiety with very low focus")

    if sleep_hours <= RISK_SLEEP_THRESHOLD and energy <= RISK_ENERGY_THRESHOLD:
        return StateResult("risk", "very low sleep with very low energy")

    if mood <= RISK_MOOD_THRESHOLD and anxiety >= RISK_ANXIETY_THRESHOLD:
        return StateResult("risk", "very low mood with high anxiety")

    # Review warning signals before returning a stable state
    if sleep_hours < WARNING_SLEEP_THRESHOLD:
        return StateResult("warning", "sleep slightly low")

    if anxiety >= WARNING_ANXIETY_THRESHOLD:
        return StateResult("warning", "anxiety elevated")

    if energy <= WARNING_ENERGY_THRESHOLD:
        return StateResult("warning", "energy low")

    if focus <= WARNING_FOCUS_THRESHOLD:
        return StateResult("warning", "focus low")

    if mood <= WARNING_MOOD_THRESHOLD:
        return StateResult("warning", "mood slightly low")

    return StateResult("stable", "metrics look stable")


def analyze_state(record: Record, history: list[Record]) -> AnalysisResult:
    """
    Combines the current state with recent-trend feedback.
    """
    current_state = detect_state(record)
    trend = analyze_history(record, history)

    return AnalysisResult(
        state=current_state.state,
        reason=current_state.reason,
        trend=trend.trend,
        trend_reason=trend.trend_reason,
        recommendation=trend.recommendation,
        recent_records_used=trend.recent_records_used,
    )


def analyze_history(current_record: Record, history: list[Record]) -> TrendResult:
    """
    Reviews recent records and detects the short-term trend.
    """
    # Build the analysis window
    combined = [*history, current_record]
    recent = combined[-RECENT_HISTORY_LIMIT:]

    # Handle the first record
    if len(recent) == 1:
        return TrendResult(
            trend="no_history_yet",
            trend_reason="first record stored, trend not available yet",
            recommendation="keep logging records so patterns can be detected",
            recent_records_used=1,
        )

    # Build state counts for streak and ratio checks
    state_sequence = [detect_state(item).state for item in recent]
    risk_count = state_sequence.count("risk")
    warning_count = state_sequence.count("warning")
    recent_records_used = len(recent)

    risk_streak = _count_tail_streak(state_sequence, "risk")
    warning_streak = _count_tail_streak(state_sequence, "warning")

    # Split records into previous and current windows
    previous_window = recent[:-TREND_WINDOW]
    current_window = recent[-TREND_WINDOW:]
    metric_shift = _compare_windows(previous_window, current_window)

    # Check for critical streaks and instability patterns
    if risk_streak >= RISK_STREAK_LIMIT:
        return TrendResult(
            trend="deteriorating",
            trend_reason="risk is repeating in consecutive records",
            recommendation="reduce pressure today and protect sleep before pushing harder",
            recent_records_used=recent_records_used,
        )

    if recent_records_used >= 3 and risk_count / recent_records_used >= HIGH_RISK_RATIO:
        return TrendResult(
            trend="unstable",
            trend_reason="risk appears too often in recent records",
            recommendation="treat this as a repeated pattern, not a one-time bad day",
            recent_records_used=recent_records_used,
        )

    # Evaluate warning patterns and fragility
    if warning_streak >= WARNING_STREAK_LIMIT:
        return TrendResult(
            trend="under_pressure",
            trend_reason="warning has repeated several times in a row",
            recommendation="make a small adjustment before warning turns into risk",
            recent_records_used=recent_records_used,
        )

    if recent_records_used >= 4 and warning_count / recent_records_used >= HIGH_WARNING_RATIO:
        return TrendResult(
            trend="fragile",
            trend_reason="recent records lean toward warning without clear risk",
            recommendation="keep the day stable and recover one variable first",
            recent_records_used=recent_records_used,
        )

    # Check overall metric direction
    if metric_shift == "worsening":
        return TrendResult(
            trend="worsening",
            trend_reason="recent averages moved in a worse direction",
            recommendation="cut unnecessary friction and stabilize sleep, energy, and focus before demanding more",
            recent_records_used=recent_records_used,
        )

    if metric_shift == "improving":
        return TrendResult(
            trend="improving",
            trend_reason="recent averages improved compared with the previous window",
            recommendation="keep the current rhythm and protect the habits behind the improvement",
            recent_records_used=recent_records_used,
        )

    return TrendResult(
        trend="stable_pattern",
        trend_reason="recent history shows no strong shift",
        recommendation="keep tracking records to confirm the pattern",
        recent_records_used=recent_records_used,
    )


def _count_tail_streak(states: list[str], target: str) -> int:
    """
    Counts a state streak from the end of the list.
    """
    streak = 0
    for state in reversed(states):
        if state != target:
            break
        streak += 1
    return streak


def _compare_windows(previous: list[Record], current: list[Record]) -> str:
    """
    Compares two windows and returns the shift direction.
    """
    # Skip comparison if either window is too small
    if len(previous) < 2 or len(current) < 2:
        return "flat"

    # Compute average values for the main signals
    previous_sleep = mean(item.sleep_hours for item in previous)
    current_sleep = mean(item.sleep_hours for item in current)

    previous_mood = mean(item.mood for item in previous)
    current_mood = mean(item.mood for item in current)

    previous_energy = mean(item.energy for item in previous)
    current_energy = mean(item.energy for item in current)

    previous_focus = mean(item.focus for item in previous)
    current_focus = mean(item.focus for item in current)

    previous_anxiety = mean(item.anxiety for item in previous)
    current_anxiety = mean(item.anxiety for item in current)

    # Score worsening and improvement signals
    worsening_points = 0
    improving_points = 0

    if previous_sleep - current_sleep >= WORSENING_DELTA:
        worsening_points += 1
    elif current_sleep - previous_sleep >= IMPROVING_DELTA:
        improving_points += 1

    if previous_mood - current_mood >= WORSENING_DELTA:
        worsening_points += 1
    elif current_mood - previous_mood >= IMPROVING_DELTA:
        improving_points += 1

    if previous_energy - current_energy >= WORSENING_DELTA:
        worsening_points += 1
    elif current_energy - previous_energy >= IMPROVING_DELTA:
        improving_points += 1

    if previous_focus - current_focus >= WORSENING_DELTA:
        worsening_points += 1
    elif current_focus - previous_focus >= IMPROVING_DELTA:
        improving_points += 1

    # Anxiety is reversed: higher is worse, lower is better.
    if current_anxiety - previous_anxiety >= WORSENING_DELTA:
        worsening_points += 1
    elif previous_anxiety - current_anxiety >= IMPROVING_DELTA:
        improving_points += 1

    if worsening_points >= 2:
        return "worsening"
    if improving_points >= 2:
        return "improving"
    return "flat"