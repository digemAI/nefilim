from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from config import DEFAULT_STORAGE_PATH
from core.logger import build_logger
from data.schema import Record, record_from_dict

log = build_logger()


def load_history(path: str = DEFAULT_STORAGE_PATH) -> list[dict[str, Any]]:
    """
    Loads the stored history from the history file.
    Returns an empty list when the file is missing or unreadable.
    """
    file_path = Path(path)

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            return []

        data = json.loads(content)
        if not isinstance(data, list):
            log.warning("History file is not a valid list. Returning empty history.")
            return []

        return data

    except json.JSONDecodeError:
        log.warning("History file has invalid JSON. Returning empty history.")
        return []
    except OSError as error:
        log.error(f"Failed to read the history file: {error}")
        return []


def load_record_history(path: str = DEFAULT_STORAGE_PATH) -> list[Record]:
    """
    Loads history and keeps only valid records.
    Invalid items are ignored so the analysis can continue.
    """
    records: list[Record] = []
    for item in load_history(path):
        if not isinstance(item, dict):
            continue
        record = record_from_dict(item)
        if record is not None:
            records.append(record)
    return records


def save_history(
    history: list[dict[str, Any]],
    path: str = DEFAULT_STORAGE_PATH,
) -> str:
    """
    Writes the current history to the storage file.
    Creates the storage path before saving.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(history, file, indent=2, ensure_ascii=False)
        return str(file_path)
    except OSError as error:
        log.error(f"Failed to save the history file: {error}")
        raise


def append_history(record: Record, path: str = DEFAULT_STORAGE_PATH) -> str:
    """
    Appends the current record to stored history.
    Prepares the record before saving it to file.
    """
    if not is_dataclass(record):
        raise TypeError("input must be a dataclass record")

    history = load_history(path)
    history.append(asdict(record))
    saved_path = save_history(history, path)

    log.info(f"Record appended successfully to {saved_path}")
    return saved_path
