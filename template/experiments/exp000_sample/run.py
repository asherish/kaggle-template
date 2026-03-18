"""Sample experiment demonstrating the framework.

Usage:
    python -m experiments.exp000_sample.run
    python -m experiments.exp000_sample.run exp=000
    python -m experiments.exp000_sample.run exp=001
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path

import hydra
import wandb
from hydra.core.config_store import ConfigStore
from hydra.core.hydra_config import HydraConfig
from omegaconf import OmegaConf

from utils.env import EnvConfig
from utils.git import check_git_clean, get_git_hash
from utils.logger import get_logger
from utils.timing import trace

WANDB_PROJECT = "{{ wandb_project }}"
WANDB_ENTITY = "{{ wandb_entity }}"


# --- Config ---


@dataclass
class ExpConfig:
    """Experiment-specific hyperparameters."""

    debug: bool = False
    seed: int = 7
    learning_rate: float = 0.001
    batch_size: int = 32
    folds: list[int] = field(default_factory=lambda: [0, 1, 2, 3, 4])


@dataclass
class Config:
    """Top-level config combining env and exp."""

    env: EnvConfig = field(default_factory=EnvConfig)
    exp: ExpConfig = field(default_factory=ExpConfig)


cs = ConfigStore.instance()
cs.store(name="default", group="env", node=EnvConfig)
cs.store(name="default", group="exp", node=ExpConfig)


# --- Main ---


@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg: Config) -> None:
    # Duck typing: cfg is actually DictConfig but can be accessed like Config

    # --- Reproducibility: git check ---
    if not cfg.exp.debug:
        check_git_clean()
    git_hash = get_git_hash()

    # --- Derive experiment name ---
    exp_name = f"{Path(sys.argv[0]).parent.name}/{HydraConfig.get().runtime.choices.exp}"

    # --- Setup output ---
    output_dir = Path(cfg.env.exp_output_dir) / exp_name
    output_dir.mkdir(parents=True, exist_ok=True)

    logger = get_logger(__name__, output_dir)
    logger.info("Experiment: %s", exp_name)
    logger.info("Git hash: %s", git_hash)
    logger.info("Config:\n%s", OmegaConf.to_yaml(cfg))

    # --- wandb init ---
    wandb.init(
        project=WANDB_PROJECT,
        entity=WANDB_ENTITY,
        name=exp_name,
        notes=", ".join(HydraConfig.get().overrides.task),
        config={
            **OmegaConf.to_container(cfg, resolve=True),
            "git_hash": git_hash,
        },
        mode="disabled" if cfg.exp.debug else "online",
    )

    # --- Training loop placeholder ---
    with trace("training"):
        for fold in cfg.exp.folds:
            logger.info("Processing fold %d", fold)
            # TODO: Implement training logic here

    wandb.finish()
    logger.info("Done")


if __name__ == "__main__":
    main()
