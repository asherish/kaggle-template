# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright", "click"]
# ///
"""Login to Kaggle via Playwright and save session cookies.

Run this script manually to authenticate. Credentials are entered
interactively and never stored.

Usage:
    uv run tools/kaggle_login.py

Prerequisites:
    playwright install chromium

The session state is saved to ~/.kaggle/playwright_state.json
and can be reused by other tools without re-authenticating.
"""

import json
import stat
from pathlib import Path

import click
from playwright.sync_api import sync_playwright

STATE_PATH = Path.home() / ".kaggle" / "playwright_state.json"
SCREENSHOT_PATH = Path.home() / ".kaggle" / "playwright_login_result.png"


@click.command()
def main() -> None:
    """Save Kaggle session cookies to ~/.kaggle/playwright_state.json."""
    email = click.prompt("Kaggle Email / Username")
    password = click.prompt("Kaggle Password", hide_input=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context()
            page = context.new_page()

            page.goto("https://www.kaggle.com/account/login", wait_until="domcontentloaded")
            page.wait_for_timeout(8000)

            page.get_by_role("button", name="Sign in with Email").click()
            page.wait_for_timeout(3000)

            page.get_by_role("textbox", name="Email / Username").fill(email)
            page.get_by_role("textbox", name="Password").fill(password)

            page.get_by_role("button", name="Sign In").click()
            page.wait_for_timeout(10000)

            click.echo(f"Current URL: {page.url}")

            state = context.storage_state()
            STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            STATE_PATH.write_text(json.dumps(state, indent=2))
            STATE_PATH.chmod(stat.S_IRUSR | stat.S_IWUSR)
            click.echo(f"Session saved to {STATE_PATH} (chmod 600)")

        except Exception as e:
            page.screenshot(path=str(SCREENSHOT_PATH))
            click.echo(f"Error during login: {e}", err=True)
            click.echo(f"Screenshot saved to {SCREENSHOT_PATH}", err=True)
            raise SystemExit(1) from None
        finally:
            browser.close()


if __name__ == "__main__":
    main()
