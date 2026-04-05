"""Upload experiment model artifacts to Kaggle Datasets."""

import json
import shutil
import tempfile
from fnmatch import fnmatch
from pathlib import Path

import click


def _copy_matching_files(src_dir: Path, dst_dir: Path, patterns: list[str]) -> int:
    """Copy files matching any of the glob patterns, preserving directory structure.

    Returns the number of files copied.
    """
    count = 0
    for path in src_dir.rglob("*"):
        if path.is_file() and any(fnmatch(path.name, p) for p in patterns):
            rel = path.relative_to(src_dir)
            dest = dst_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
            count += 1
    return count


@click.command()
@click.option("--title", default="{{ project_name }}-model", help="Kaggle dataset title.")
@click.option("--dir", "src_dir", default="./output/experiments", help="Source directory to scan.")
@click.option(
    "--patterns",
    default="best_model.pt,best_model.pth,best_model.bin",
    help="Comma-separated file name patterns to include.",
)
@click.option("--user-name", default="{{ kaggle_username }}", help="Kaggle username.")
@click.option("--new", "is_new", is_flag=True, help="Create a new dataset instead of updating.")
def main(title: str, src_dir: str, patterns: str, user_name: str, is_new: bool) -> None:
    """Upload model artifacts to Kaggle Datasets."""
    from kaggle.api.kaggle_api_extended import KaggleApi

    pattern_list = [p.strip() for p in patterns.split(",")]
    src_path = Path(src_dir)

    if not src_path.exists():
        click.echo(f"Source directory not found: {src_path}", err=True)
        raise SystemExit(1)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        count = _copy_matching_files(src_path, tmp_path, pattern_list)

        if count == 0:
            click.echo("No files matched the specified patterns.", err=True)
            raise SystemExit(1)

        click.echo(f"Copied {count} files to staging area.")

        # Write dataset metadata
        slug = f"{user_name}/{title}"
        metadata = {
            "title": title,
            "id": slug,
            "licenses": [{"name": "CC0-1.0"}],
        }
        (tmp_path / "dataset-metadata.json").write_text(json.dumps(metadata, indent=2))

        # Upload
        api = KaggleApi()
        api.authenticate()

        if is_new:
            api.dataset_create_new(str(tmp_path), dir_mode="tar", quiet=False)
            click.echo(f"Created new dataset: {slug}")
        else:
            api.dataset_create_version(str(tmp_path), version_notes="update", dir_mode="tar", quiet=False)
            click.echo(f"Updated dataset: {slug}")


if __name__ == "__main__":
    main()
