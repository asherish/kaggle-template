"""Common experiment setup: git check, output directory, logger, and W&B initialization."""

import dataclasses
import logging
from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

from utils.git import check_git_clean, get_git_hash
from utils.logger import get_logger

WANDB_PROJECT = "{{ wandb_project }}"
WANDB_ENTITY = "{{ wandb_entity }}"


@dataclasses.dataclass(frozen=True)
class ExperimentContext:
    """Read-only context produced by experiment setup."""

    output_dir: Path
    logger: logging.Logger
    git_hash: str
    exp_name: str
    timestamp: str


@contextmanager
def run_experiment(
    *,
    experiment_dir: Path,
    params_dict: dict,
    debug: bool,
    config_path: str | None = None,
) -> Generator[ExperimentContext, None, None]:
    """Set up and tear down a single experiment run.

    Performs git-clean check (skipped in debug mode), creates output directory,
    initializes logger and W&B, then yields an ExperimentContext. On exit,
    W&B is finalized regardless of whether the training succeeded.

    Args:
        experiment_dir: Path to the experiment directory (typically
            ``Path(__file__).resolve().parent`` from the calling run.py).
        params_dict: Serialized experiment parameters (from ``params.model_dump()``).
        debug: If True, skip git check and disable W&B logging.
        config_path: Path to the config file. If provided, this file is excluded
            from the git-clean check so config edits don't block a run.
    """
    project_root = experiment_dir.parent.parent
    exp_name = experiment_dir.name

    # --- Git check ---
    if not debug:
        allowed: set[str] | None = None
        if config_path is not None:
            allowed = {str(Path(config_path).resolve().relative_to(project_root))}
        check_git_clean(allowed_files=allowed)
    git_hash = get_git_hash()

    # --- Output directory ---
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    output_dir = project_root / "output" / "experiments" / exp_name / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- Logger ---
    logger = get_logger(exp_name, output_dir, timestamp=timestamp)
    logger.info("Experiment: %s", exp_name)
    logger.info("Git hash: %s", git_hash)
    logger.info("Config: %s", params_dict)

    # --- W&B ---
    import wandb

    wandb.init(
        project=WANDB_PROJECT,
        entity=WANDB_ENTITY,
        name=f"{exp_name}/{timestamp}",
        config={**params_dict, "git_hash": git_hash},
        mode="disabled" if debug else "online",
    )

    ctx = ExperimentContext(
        output_dir=output_dir,
        logger=logger,
        git_hash=git_hash,
        exp_name=exp_name,
        timestamp=timestamp,
    )

    try:
        yield ctx
    finally:
        wandb.finish()
        logger.info("Done")
