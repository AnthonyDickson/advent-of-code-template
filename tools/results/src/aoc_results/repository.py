"""Find the repository, list its templates, and work out where a solution came from."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

TEMPLATE_DIRNAME = "template"
REPO_MARKER = "flake.nix"
DAY_FOLDER = re.compile(r"^\d{4}-day-(?P<day>\d{1,2})$")


class RepositoryError(Exception):
    """Raised when the repository layout or a solution folder cannot be used."""


def discover(start: Path | None = None) -> Path:
    """Return the repository root containing ``template/``, walking up from *start*."""
    origin = (start or Path.cwd()).expanduser().resolve()
    for candidate in (origin, *origin.parents):
        if (candidate / TEMPLATE_DIRNAME).is_dir() and (candidate / REPO_MARKER).is_file():
            return candidate
    raise RepositoryError(
        f"no Advent of Code repository (template/ plus {REPO_MARKER}) found above {origin}"
    )


def languages(repo: Path) -> list[str]:
    """Every language with a template, sorted so rows and messages stay stable."""
    root = repo / TEMPLATE_DIRNAME
    if not root.is_dir():
        raise RepositoryError(f"{root} does not exist")
    return sorted(
        entry.name for entry in root.iterdir() if entry.is_dir() and not entry.name.startswith(".")
    )


def detect_language(repo: Path, solution: Path) -> str:
    """The template *solution* was copied from, judging by the files it holds."""
    present = source_files(solution)
    candidates = [
        (len(needed), language)
        for language in languages(repo)
        if (needed := source_files(repo / TEMPLATE_DIRNAME / language)) and needed <= present
    ]
    if not candidates:
        raise RepositoryError(
            f"{solution} matches no template; pass --language to name the one it was copied from"
        )

    candidates.sort(key=lambda candidate: (-candidate[0], candidate[1]))
    best = candidates[0]
    if len(candidates) > 1 and candidates[1][0] == best[0]:
        raise RepositoryError(
            f"{solution} matches both {best[1]!r} and {candidates[1][1]!r}; pass --language"
        )
    return best[1]


def detect_day(solution: Path) -> int:
    """The puzzle day in a ``<year>-day-<dd>`` folder name."""
    match = DAY_FOLDER.match(solution.name)
    if match is None:
        raise RepositoryError(
            f"cannot read a day from {solution.name!r}; pass --day, or name the folder <year>-day-<dd>"
        )
    return int(match["day"])


def source_files(directory: Path) -> frozenset[str]:
    """Every file git does not ignore in *directory*, relative to that directory.

    Git already knows what a template or solution is made of: each template ships a
    ``.gitignore`` for its build output and the repository ignores ``**/input.txt``. Asking it
    also keeps a template's working tree free of ignored build output without a hand-kept list,
    and ``--others`` includes files that are not committed yet, which is how a freshly
    bootstrapped solution is read.
    """
    listing = _run_git(directory, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    return frozenset(name for name in listing.split("\0") if name)


def _run_git(directory: Path, *arguments: str) -> str:
    """Run git in *directory* and return its stdout, raising a ``RepositoryError`` on failure."""
    try:
        completed = subprocess.run(
            ("git", "-C", str(directory), *arguments), capture_output=True, check=True, text=True
        )
    except FileNotFoundError as error:
        raise RepositoryError("`git` is not on PATH; run this inside a dev shell") from error
    except subprocess.CalledProcessError as error:
        raise RepositoryError(
            f"`git {arguments[0]}` failed in {directory}:\n{error.stderr.strip()}"
        ) from error
    return completed.stdout
