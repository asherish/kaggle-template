"""Environment configuration shared across all experiments."""

from dataclasses import dataclass, field
from pathlib import Path


def _project_root() -> Path:
    """Return the project root directory (parent of utils/)."""
    return Path(__file__).resolve().parent.parent


@dataclass
class EnvConfig:
    """Paths and environment settings.

    All paths are relative to the project root by default.
    """

    input_dir: str = field(default_factory=lambda: str(_project_root() / "input"))
    output_dir: str = field(default_factory=lambda: str(_project_root() / "output"))
    exp_output_dir: str = field(default_factory=lambda: str(_project_root() / "output" / "experiments"))
