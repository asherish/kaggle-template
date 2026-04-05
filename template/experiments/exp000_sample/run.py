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
from pydantic import BaseModel, Field, field_validator

from utils.experiment import run_experiment
from utils.timing import trace

EXPERIMENT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = EXPERIMENT_DIR / "config.yaml"


class Params(BaseModel):
    """Experiment hyperparameters with validation."""

    debug: bool = False
    seed: int = 7
    learning_rate: float = Field(default=0.001, gt=0)
    batch_size: int = Field(default=32, gt=0)
    folds: list[int] = Field(default=[0, 1, 2, 3, 4])

    @field_validator("folds", mode="before")
    @classmethod
    def parse_folds(cls, v: str | list[int]) -> list[int]:
        """Accept comma-separated string (e.g. '0,1,2') or list."""
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",")]
        return v


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
    with open(config_path) as f:
        raw: dict = yaml.safe_load(f) or {}

    overrides = {"debug": debug, "seed": seed, "learning_rate": learning_rate, "batch_size": batch_size, "folds": folds}
    raw.update({k: v for k, v in overrides.items() if v is not None})
    params = Params(**raw)

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
