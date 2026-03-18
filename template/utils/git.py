"""Git utilities for experiment reproducibility."""

import subprocess


class GitDirtyError(Exception):
    """Raised when the working tree has uncommitted changes."""


def check_git_clean() -> None:
    """Raise GitDirtyError if the git working tree is dirty.

    Checks staged, unstaged, and untracked files via ``git status --porcelain``.
    """
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    if result.stdout.strip():
        raise GitDirtyError(
            "Working tree has uncommitted changes. "
            "Commit or stash changes before running experiments.\n"
            f"Dirty files:\n{result.stdout}"
        )


def get_git_hash() -> str:
    """Return the current HEAD commit hash (short form)."""
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()
