"""Weighted random selection between the available templates."""

from __future__ import annotations

import random
from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    """One language on the wheel."""

    language: str
    weight: float
    chance: float

    @property
    def percent(self) -> float:
        """Probability of this language being drawn, as a percentage."""
        return self.chance * 100


class Lottery:
    """A weighted draw over languages.

    Weights are relative: a language with weight 2 is twice as likely to come up as one with weight
    1. A weight of 0 removes a language from the wheel entirely.
    """

    def __init__(self, weights: Mapping[str, float], *, rng: random.Random | None = None) -> None:
        self._rng = rng if rng is not None else random.Random()
        self.entries = _build_entries(weights)

    def draw(self) -> Entry:
        """Pick one entry, honouring the weights."""
        return self._rng.choices(
            self.entries, weights=[entry.weight for entry in self.entries], k=1
        )[0]

    def row_of(self, language: str) -> int:
        """Index of *language* in the wheel."""
        for row, entry in enumerate(self.entries):
            if entry.language == language:
                return row
        raise KeyError(language)


def _build_entries(weights: Mapping[str, float]) -> tuple[Entry, ...]:
    drawn = sorted((str(language), float(weight)) for language, weight in weights.items())
    positive = [(language, weight) for language, weight in drawn if weight > 0]
    if not positive:
        raise ValueError("at least one language needs a weight above zero")

    total = sum(weight for _, weight in positive)
    return tuple(Entry(language, weight, weight / total) for language, weight in positive)
