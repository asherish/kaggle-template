"""Download competition dataset from Kaggle."""

import zipfile
from pathlib import Path

import click


def _extract_and_remove_zips(directory: Path) -> int:
    """Extract all zip files in directory and remove the archives."""
    count = 0
    for zip_path in directory.glob("*.zip"):
        click.echo(f"Extracting {zip_path.name}...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(directory)
        zip_path.unlink()
        count += 1
    return count


@click.command()
@click.option("--competition", default="{{ kaggle_competition }}", help="Kaggle competition slug.")
@click.option("--dest", default="./input/{{ kaggle_competition }}", help="Destination directory.")
@click.option("--file", "file_name", default=None, help="Download a single file instead of all files.")
@click.option("--unzip", is_flag=True, help="Extract zip files after download.")
@click.option("--force", is_flag=True, help="Force re-download even if files exist.")
def main(competition: str, dest: str, file_name: str | None, unzip: bool, force: bool) -> None:
    """Download competition dataset from Kaggle."""
    from kaggle.api.kaggle_api_extended import KaggleApi

    dest_path = Path(dest)

    if dest_path.exists() and any(dest_path.iterdir()) and not force:
        click.echo(f"Data already exists at {dest_path}. Use --force to re-download.", err=True)
        raise SystemExit(1)

    dest_path.mkdir(parents=True, exist_ok=True)

    api = KaggleApi()
    api.authenticate()

    if file_name:
        click.echo(f"Downloading {file_name} from {competition}...")
        api.competition_download_file(competition, file_name, path=str(dest_path), force=force, quiet=False)
    else:
        click.echo(f"Downloading all files from {competition}...")
        api.competition_download_files(competition, path=str(dest_path), force=force, quiet=False)

    if unzip:
        count = _extract_and_remove_zips(dest_path)
        click.echo(f"Extracted {count} zip archive(s).")

    click.echo(f"Done. Files saved to {dest_path}")


if __name__ == "__main__":
    main()
