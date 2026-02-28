# handles persistence of nefilim check-in records in json format
import json
import os
from typing import Any, Dict, List


def _load_history(path: str) -> List[Dict[str, Any]]:
    """
    loads existing history from disk.
    returns an empty list if the file does not exist or is invalid.
    """

    # if file does not exist, return empty history
    if not os.path.exists(path):
        return []

    try:
        # read json content from file
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # ensure data structure is a list
        return data if isinstance(data, list) else []

    except json.JSONDecodeError:
        # return empty list if file is corrupted
        return []

def append_history(path: str, record: Dict[str, Any]) -> None:
    """
    appends a new check-in record to the history file.
    """

    # load current history
    history = _load_history(path)

    # append new record
    history.append(record)

    # ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # write updated history back to disk
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)