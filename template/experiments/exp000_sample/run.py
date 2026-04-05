"""Sample experiment demonstrating the framework.

Usage:
    python -m experiments.exp000_sample.run
    python -m experiments.exp000_sample.run --debug
    python -m experiments.exp000_sample.run --seed 42 --lr 0.01
    python -m experiments.exp000_sample.run --config path/to/other.yaml
"""

from pathlib import Path

import click
import yaml
from pydantic import BaseModel, Field

from utils.experiment import run_experiment
from utils.timing import trace

EXPERIMENT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = EXPERIMENT_DIR / "config.yaml"


# --- Config ---


class Params(BaseModel):
    """Experiment hyperparameters with validation."""

    debug: bool = False
    seed: int = 7
    learning_rate: float = Field(default=0.001, gt=0)
    batch_size: int = Field(default=32, gt=0)
    folds: list[int] = Field(default=[0, 1, 2, 3, 4])


# --- Main ---


@click.command()
@click.option("--config", "-c", "config_path", default=str(DEFAULT_CONFIG), type=click.Path(exists=True))
@click.option("--debug", is_flag=True, default=None, help="Disable git check and W&B logging.")
@click.option("--seed", type=int, default=None)
@click.option("--lr", "--learning-rate", "learning_rate", type=float, default=None)
@click.option("--batch-size", type=int, default=None)
@click.option("--folds", type=str, default=None, help="Comma-separated fold indices, e.g. '0,1,2'.")
def main(
    config_path: str,
    debug: bool | None,
    seed: int | None,
    learning_rate: float | None,
    batch_size: int | None,
    folds: str | None,
) -> None:
    # --- Load config ---
    with open(config_path) as f:
        raw: dict = yaml.safe_load(f) or {}

    # --- Apply CLI overrides ---
    if debug is not None:
        raw["debug"] = debug
    if seed is not None:
        raw["seed"] = seed
    if learning_rate is not None:
        raw["learning_rate"] = learning_rate
    if batch_size is not None:
        raw["batch_size"] = batch_size
    if folds is not None:
        raw["folds"] = [int(f) for f in folds.split(",")]

    params = Params(**raw)

    # --- Run experiment ---
    with run_experiment(
        experiment_dir=EXPERIMENT_DIR,
        params_dict=params.model_dump(),
        debug=params.debug,
        config_path=config_path,
    ) as ctx, trace("training"):
        for fold in params.folds:
            ctx.logger.info("Processing fold %d", fold)
            # TODO: Implement training logic here


if __name__ == "__main__":
    main()
