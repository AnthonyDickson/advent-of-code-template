"""Everything a draw needs: the repository, the weighted wheel and the shell to print."""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

from aoc_lottery.config import discover_repo, resolve_weights
from aoc_lottery.guidance import preferred_shell
from aoc_lottery.lottery import Lottery


@dataclass(frozen=True)
class Session:
    """State shared by the TUI and the plain CLI."""

    repo: Path
    lottery: Lottery
    shell: str


def build_session(
    *,
    repo: Path | None = None,
    config: Path | None = None,
    seed: int | None = None,
    shell: str | None = None,
) -> Session:
    """Resolve the repository, load the weights and prepare the wheel."""
    root = discover_repo(repo) if repo is not None else discover_repo()
    weights = resolve_weights(root, config.expanduser() if config is not None else None)
    return Session(
        repo=root,
        lottery=Lottery(weights, rng=random.Random(seed)),
        shell=shell or preferred_shell(),
    )
