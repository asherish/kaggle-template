# CLAUDE.md

## Project: {{ project_name }}

Kaggle competition project using Click + Pydantic + wandb for experiment management.

## Architecture

- `experiments/` — Each experiment is a directory (`exp000_name/`) containing `run.py` + `config.yaml`
- `utils/` — Shared infrastructure (git, logger, timing) — keep minimal
- `tools/` — CLI tools for Kaggle API (upload model, check submission)
- Run experiments with: `python -m experiments.exp000_sample.run`

## Rules

- Always run `ruff format` and `ruff check --fix` before committing
- Run `ty check` for type checking
- Never modify files in `input/` (read-only competition data)
- Experiment `run.py` calls `check_git_clean()` before training — commit code changes first (config.yaml edits are allowed)
- Use Pydantic BaseModel for config validation (no raw dicts)
- All code comments and docstrings in English

## Conventions

- Python 3.11
- Line length: 120
- Use `pathlib.Path`, not `os.path`
- Type hints on all function signatures
- Click + Pydantic for configuration (no argparse)
- Module execution: `python -m experiments.<name>.run`
