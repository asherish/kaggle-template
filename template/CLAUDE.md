# CLAUDE.md

## Project: {{ project_name }}

Kaggle competition project using Hydra + wandb for experiment management.

## Architecture

- `experiments/` — Each experiment is a directory (`exp000_name/`) containing `run.py` + configs
- `utils/` — Shared infrastructure (env, git, logger, timing) — keep minimal
- `tools/` — CLI tools for Kaggle API (upload model, check submission)
- Run experiments with: `python -m experiments.exp000_sample.run exp=000`

## Rules

- Always run `ruff format` and `ruff check --fix` before committing
- Run `ty check` for type checking
- Never modify files in `input/` (read-only competition data)
- Experiment `run.py` calls `check_git_clean()` before training — commit first
- Use dataclasses for all configs (no raw dicts)
- All code comments and docstrings in English

## Conventions

- Python 3.10 (matches Kaggle environment)
- Line length: 120
- Use `pathlib.Path`, not `os.path`
- Type hints on all function signatures
- Hydra + dataclass for configuration (no argparse)
- Module execution: `python -m experiments.<name>.run`
