from datetime import datetime
import config
from core.state_detector import detect_state
from data.storage import append_history


def main() -> None:
    """
    entry point for nefilim v1.
    creates a sample check-in, evaluates state,
    and persists the result to the json history file.
    """

    # sample input for v1 (temporary test data), later this will come from cli or user input
    sample_checkin = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "sleep_hours": 6.0,
        "stress": 7,
        "anxiety": 5,
        "energy": 5,
        "focus": 4,
        "motivation": 5,
    }

    # evaluate psychological state based on thresholds
    result = detect_state(
        sleep_hours=float(sample_checkin["sleep_hours"]),
        stress=int(sample_checkin["stress"]),
        anxiety=int(sample_checkin["anxiety"]),
    )

    # attach detected state to record
    sample_checkin["state"] = result.state

    # persist record to history file
    append_history(config.HISTORY_FILE_PATH, sample_checkin)

    # console output for verification (v1 test mode)
    print("nefilim v1 (test mode)")
    print(f"state: {result.state}")
    print(f"reason: {result.reason}")
    print(f"saved_to: {config.HISTORY_FILE_PATH}")

# script entry point
if __name__ == "__main__":
    main()