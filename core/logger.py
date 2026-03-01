from __future__ import annotations
import logging


def build_logger(name: str = "nefilim") -> logging.Logger:
    """
    Creates and configures a logger instance.

    - Prevents duplicate handlers
    - Sets default level to INFO
    - Applies consistent console formatting

    Returns:
        logging.Logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers if logger already configured
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False  # Prevent duplicate logs in root logger

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s - %(message)s",
        datefmt="%H:%M:%S"
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger