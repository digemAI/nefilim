import json
import os
from typing import Any, Dict, List


def load_history(path: str) -> List[Dict[str, Any]]:
    """
    load history from disk.
    returns an empty list if the file is missing or invalid.
    """

    # Missing file → empty history
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Invalid structure → reset history
        return data if isinstance(data, list) else []

    except json.JSONDecodeError:
        # Corrupted file → reset history"""
    
        return []

def append_history(path: str, record: Dict[str, Any]) -> None:
    """
    Append a new record to history.
    """

    # Load existing history
    history = load_history(path)
    
    history.append(record)

    # Create directory if needed
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Save updated history
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)