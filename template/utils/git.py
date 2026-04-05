"""Git utilities for experiment reproducibility."""

import subprocess


class GitDirtyError(Exception):
    """Raised when the working tree has uncommitted changes."""


def check_git_clean(*, allowed_files: set[str] | None = None) -> None:
    """Raise GitDirtyError if the git working tree is dirty.

    Checks staged, unstaged, and untracked files via ``git status --porcelain``.
    Files listed in *allowed_files* (paths relative to the repo root) are
    ignored so that config files can be modified without blocking a run.
    """
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    if not result.stdout.strip():
        return

    dirty: list[str] = []
    for line in result.stdout.strip().splitlines():
        # porcelain format: "XY filename" (3-char prefix)
        filename = line[3:]
        if allowed_files and filename in allowed_files:
            continue
        dirty.append(line)

    if dirty:
        raise GitDirtyError(
            "Working tree has uncommitted changes. "
            "Commit or stash changes before running experiments.\n"
            "Dirty files:\n" + "\n".join(dirty)
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
