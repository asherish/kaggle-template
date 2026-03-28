"""Set up Kaggle API token for authentication."""

import stat
import webbrowser
from pathlib import Path

import click

KAGGLE_SETTINGS_URL = "https://www.kaggle.com/settings"
TOKEN_PATH = Path.home() / ".kaggle" / "access_token"


@click.command()
@click.option("--browse", is_flag=True, help="Open Kaggle settings page in browser.")
def main(browse: bool) -> None:
    """Save a Kaggle API token to ~/.kaggle/access_token."""
    if TOKEN_PATH.exists():
        if not click.confirm(f"Token already exists at {TOKEN_PATH}. Overwrite?"):
            raise SystemExit(0)

    if browse:
        click.echo(f"Opening {KAGGLE_SETTINGS_URL} ...")
        webbrowser.open(KAGGLE_SETTINGS_URL)

    click.echo('Go to Kaggle Settings > API > "Generate New Token" and copy the token.')
    token = click.prompt("Paste your API token", hide_input=True).strip()

    if not token:
        click.echo("Empty token. Aborted.", err=True)
        raise SystemExit(1)

    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(token)
    TOKEN_PATH.chmod(stat.S_IRUSR | stat.S_IWUSR)

    click.echo(f"Saved token to {TOKEN_PATH} (chmod 600)")


if __name__ == "__main__":
    main()
