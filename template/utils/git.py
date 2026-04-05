"""Git utilities for experiment reproducibility."""

import subprocess
from pathlib import Path


class GitError(Exception):
    """Base class for git-related errors."""


class GitDirtyError(GitError):
    """Raised when the working tree has uncommitted changes."""


def _run_git(*args: str) -> str:
    """Run a git command and return stripped stdout.

    Raises GitError with a user-friendly message if the command fails.
    """
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise GitError(
            f"git {' '.join(args)} failed (exit {exc.returncode}): {exc.stderr.strip() or exc.stdout.strip()}"
        ) from exc
    return result.stdout.strip()


def get_project_root() -> Path:
    """Return the root directory of the current git repository."""
    return Path(_run_git("rev-parse", "--show-toplevel"))


def check_git_clean(*, allowed_files: set[str] | None = None) -> None:
    """Raise GitDirtyError if the git working tree is dirty.

    Checks staged, unstaged, and untracked files via ``git status --porcelain``.
    Files listed in *allowed_files* (paths relative to the repo root) are
    ignored so that config files can be modified without blocking a run.
    """
    output = _run_git("status", "--porcelain")
    if not output:
        return

    dirty: list[str] = []
    for line in output.splitlines():
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
    return _run_git("rev-parse", "--short", "HEAD")
