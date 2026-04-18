from __future__ import annotations

import logging
from pathlib import Path

from config import DEFAULT_LOG_PATH

_LOGGER_NAME = "nefilim"


def build_logger() -> logging.Logger:
    """
    Builds the logger used across the NEFILIM flow.
    Directs output to file and console.
    """
    logger = logging.getLogger(_LOGGER_NAME)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    log_path = Path(DEFAULT_LOG_PATH)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Write logs to file
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Send logs to console during execution
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger