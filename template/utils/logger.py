"""Dual logging to file and console."""

import logging
from datetime import UTC, datetime
from pathlib import Path


def get_logger(name: str, log_dir: Path | str, *, timestamp: str | None = None) -> logging.Logger:
    """Create a logger that writes to both console and a timestamped log file.

    Args:
        name: Logger name (typically the experiment name).
        log_dir: Directory where the log file will be created.
        timestamp: Optional pre-computed timestamp for the log filename.
            If None, a new timestamp is generated.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    fmt = logging.Formatter("[%(asctime)s : %(levelname)s - %(filename)s] %(message)s")

    # Console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    # File handler
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = timestamp or datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(log_dir / f"{timestamp}.log")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger
