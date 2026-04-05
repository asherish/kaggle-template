"""Performance measurement context managers."""

import logging
import sys
import time
from collections.abc import Generator
from contextlib import contextmanager

import psutil


@contextmanager
def trace(title: str, *, logger: logging.Logger | None = None) -> Generator[None, None, None]:
    """Measure execution time and memory usage of a block.

    Args:
        title: Label for the traced block.
        logger: If provided, log via logger.info instead of printing to stderr.
    """
    process = psutil.Process()
    mem_before = process.memory_info().rss / (1024**3)  # GB
    t0 = time.time()

    yield

    elapsed = time.time() - t0
    mem_after = process.memory_info().rss / (1024**3)  # GB
    msg = (
        f"[{title}] elapsed: {elapsed:.1f}s, "
        f"memory: {mem_before:.2f}GB -> {mem_after:.2f}GB (delta: {mem_after - mem_before:+.2f}GB)"
    )
    if logger:
        logger.info(msg)
    else:
        print(msg, file=sys.stderr)


@contextmanager
def timer(title: str, *, logger: logging.Logger | None = None) -> Generator[None, None, None]:
    """Measure execution time of a block.

    Args:
        title: Label for the timed block.
        logger: If provided, log via logger.info instead of printing to stderr.
    """
    t0 = time.time()
    yield
    msg = f"[{title}] {time.time() - t0:.1f}s"
    if logger:
        logger.info(msg)
    else:
        print(msg, file=sys.stderr)
