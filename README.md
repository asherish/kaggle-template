# kaggle-template

Copier-based template for Kaggle competition projects.

## Features

- **Experiment management**: Hydra + dataclass structured configs (major/minor versioning)
- **Reproducibility**: Git dirty check before training, git hash logged to wandb
- **Tracking**: Weights & Biases integration
- **ML libraries**: PyTorch, Lightning, Transformers, LightGBM, XGBoost, CatBoost
- **Docker**: Kaggle official GPU/CPU images
- **Package management**: uv
- **Task runner**: mise
- **Code quality**: ruff + ty via pre-commit and Claude Code hooks
- **Kaggle tools**: Model upload to Kaggle Datasets, submission status monitoring

## Usage

### Create a new project

```bash
uvx copier copy gh:asherish/kaggle-template my-competition
```

### Update an existing project with template changes

```bash
cd my-competition
uvx copier update -A
```

## Template variables

| Variable | Description | Default |
|---|---|---|
| `project_name` | Competition/project name | (required) |
| `kaggle_competition` | Kaggle competition slug | same as project_name |
| `kaggle_username` | Your Kaggle username | (required) |
| `wandb_project` | W&B project name | same as project_name |
| `wandb_entity` | W&B entity (user/team) | same as kaggle_username |
| `author_name` | Author name | (required) |
| `kaggle_image_version` | Kaggle GPU image tag | v160 |

## License

MIT
