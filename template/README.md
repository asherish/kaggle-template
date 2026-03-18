# {{ project_name }}

Kaggle competition project for **{{ kaggle_competition }}**.

## Setup

### Local (uv)

```bash
mise run uv-setup
```

### Docker (GPU)

```bash
mise run docker-build
mise run docker-bash
```

### Docker (CPU)

```bash
mise run docker-build-cpu
```

## Running Experiments

```bash
# Run with default config
python -m experiments.exp000_sample.run

# Run with a specific minor version
python -m experiments.exp000_sample.run exp=000

# Run in debug mode (skips git dirty check)
python -m experiments.exp000_sample.run exp=000 exp.debug=true
```

### Creating a New Experiment

1. Copy `experiments/exp000_sample/` to `experiments/exp001_yourname/`
2. Edit `run.py`: define your `ExpConfig` dataclass and training logic
3. Add minor version configs in `exp/000.yaml`, `exp/001.yaml`, ...
4. Run: `python -m experiments.exp001_yourname.run exp=000`

## Kaggle Tools

```bash
# Upload model artifacts to Kaggle Datasets
mise run upload-model

# Monitor latest submission status
mise run check-submission
```

## Code Quality

```bash
mise run fmt           # ruff format + check
mise run type-check    # ty check
mise run test          # pytest
```

## Installing Optional Libraries

### PyTorch Geometric

```bash
uv add torch-geometric
# Install extensions matching your torch + CUDA versions:
# See https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html
```

### nnUNet

```bash
uv add nnunetv2
```

## License

MIT
