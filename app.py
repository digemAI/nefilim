from datetime import datetime
import config
from core.state_detector import detect_state
from data.storage import append_history


def main() -> None:
    """
    entry point for nefilim v1.
    creates sample data, evaluates state,
    and save the result to the json history file.
    """

    # Temporary test input    
    sample_record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "sleep_hours": 6.0,
        "stress": 7,
        "anxiety": 5,
        "energy": 5,
        "focus": 4,
        "motivation": 5,
    }

    # Detect current state
    result = detect_state(
        sleep_hours=float(sample_record["sleep_hours"]),
        stress=int(sample_record["stress"]),
        anxiety=int(sample_record["anxiety"]),
    )

    # Add detected state to the record    
    sample_record["state"] = result.state

    # Save the record to the history file
    append_history(config.HISTORY_FILE_PATH, sample_record)

    # v1 verification output
    print("nefilim v1 (test mode)")
    print(f"state: {result.state}")
    print(f"reason: {result.reason}")
    print(f"saved_to: {config.HISTORY_FILE_PATH}")

# entry point
if __name__ == "__main__":
    main()