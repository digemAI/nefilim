from dataclasses import dataclass
import config

@dataclass(frozen=True)
class StateResult:
    """
    Result of the state detector.
    """
    state: str      # "stable" | "warning" | "risk"
    reason: str     # short explanation of the decision


def detect_state(sleep_hours: float, stress: int, anxiety: int) -> StateResult:
    """
    Detect system state from input metrics.
    """

    # risk conditions (highest priority)

    # sleep below safe level
    if sleep_hours < config.RISK_SLEEP_THRESHOLD:
        return StateResult(
            "risk",
            "sleep critically low"
        )

    # stress dangerously high
    if stress >= config.RISK_STRESS_THRESHOLD:
        return StateResult(
            "risk",
            "stress critically high"
        )

     # anxiety dangerously high 
    if anxiety >= config.RISK_ANXIETY_THRESHOLD:
        return StateResult(
            "risk",
            "anxiety critically high"
        )

    # warning conditions

     # sleep in warning range
    if config.WARNING_SLEEP_MIN <= sleep_hours <= config.WARNING_SLEEP_MAX:
        return StateResult(
            "warning",
            "sleep slightly low"        
        )
    
    # stress in warning range
    if config.WARNING_STRESS_MIN <= stress <= config.WARNING_STRESS_MAX:
        return StateResult(
            "warning",
            "stress elevated"
        )

     # anxiety in warning range
    if config.WARNING_ANXIETY_MIN <= anxiety <= config.WARNING_ANXIETY_MAX:
        return StateResult(
            "warning",
            "anxiety elevated"
        )

    # stable condition

    return StateResult(
        "stable",
        "all metrics within safe range"
    )
