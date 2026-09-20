"""Helpers for driving the Textual app in tests."""

from __future__ import annotations

import asyncio
from collections.abc import Callable

from textual.pilot import Pilot
from textual.widgets import Static


async def settle(pilot: Pilot, screen_type: type, timeout: float = 5.0) -> None:
    """Wait until *screen_type* is the active screen."""
    async with asyncio.timeout(timeout):
        while not isinstance(pilot.app.screen, screen_type):
            await pilot.pause(0.01)


async def wait_until(pilot: Pilot, predicate: Callable[[], bool], timeout: float = 5.0) -> None:
    """Wait until *predicate* holds. Focus arrives a message after a screen is pushed, for example."""
    async with asyncio.timeout(timeout):
        while not predicate():
            await pilot.pause(0.01)


def content(widget: Static) -> str:
    """The text a Static is currently showing."""
    return str(widget.render())
