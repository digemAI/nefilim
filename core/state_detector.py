from dataclasses import dataclass
import config

@dataclass(frozen=True)
class StateResult:
    """
    represents the result of the state detection process.
    """
    state: str      # "stable" | "warning" | "risk"
    reason: str     # explanation of why the state was triggered


def detect_state(sleep_hours: float, stress: int, anxiety: int) -> StateResult:
    """
    determines the system state based on predefined thresholds.
    """

    # risk conditions (highest priority)

    # sleep below critical threshold
    if sleep_hours < config.RISK_SLEEP_THRESHOLD:
        return StateResult(
            "risk",
            "critical sleep deficit detected"
        )

    # stress at or above critical threshold
    if stress >= config.RISK_STRESS_THRESHOLD:
        return StateResult(
            "risk",
            "critical stress detected"
        )

     # anxiety at or above critical threshold
    if anxiety >= config.RISK_ANXIETY_THRESHOLD:
        return StateResult(
            "risk",
            "critical anxiety detected"
        )

    # warning conditions

     # sleep inside warning interval
    if config.WARNING_SLEEP_MIN <= sleep_hours <= config.WARNING_SLEEP_MAX:
        return StateResult(
            "warning",
            "elevated sleep level"        
        )
    
    # stress inside warning interval
    if config.WARNING_STRESS_MIN <= stress <= config.WARNING_STRESS_MAX:
        return StateResult(
            "warning",
            "elevated stress level"
        )

     # anxiety inside warning interval
    if config.WARNING_ANXIETY_MIN <= anxiety <= config.WARNING_ANXIETY_MAX:
        return StateResult(
            "warning",
            "elevated anxiety level"
        )

    # stable condition

    return StateResult(
        "stable",
        "no thresholds triggered"
    )