"""Performance measurement context managers."""

import sys
import time
from collections.abc import Generator
from contextlib import contextmanager

import psutil


@contextmanager
def trace(title: str) -> Generator[None, None, None]:
    """Measure execution time and memory usage of a block.

    Prints elapsed time and memory delta to stderr.

    Args:
        title: Label for the traced block.
    """
    process = psutil.Process()
    mem_before = process.memory_info().rss / (1024**3)  # GB
    t0 = time.time()

    yield

    elapsed = time.time() - t0
    mem_after = process.memory_info().rss / (1024**3)  # GB
    print(
        f"[{title}] elapsed: {elapsed:.1f}s, "
        f"memory: {mem_before:.2f}GB -> {mem_after:.2f}GB (delta: {mem_after - mem_before:+.2f}GB)",
        file=sys.stderr,
    )


@contextmanager
def timer(title: str) -> Generator[None, None, None]:
    """Measure execution time of a block.

    Prints elapsed time to stdout.

    Args:
        title: Label for the timed block.
    """
    t0 = time.time()
    yield
    print(f"[{title}] {time.time() - t0:.1f}s")
