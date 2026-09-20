"""Drive the TUI through a whole draw, re-roll and bootstrap."""

from __future__ import annotations

from pathlib import Path

import pytest
from helpers import content, settle, wait_until
from textual.widgets import Button, DataTable, Input, Static

from aoc_lottery.app import (
    BootstrapScreen,
    LotteryApp,
    NextStepsScreen,
    ResultScreen,
    SpinTiming,
    StepsView,
    WheelScreen,
)
from aoc_lottery.lottery import Lottery
from aoc_lottery.session import Session

# Timers fire as fast as possible so the tests do not wait for the animation.
# Textual's timers cannot take a zero interval, hence the millisecond.
FAST = SpinTiming(fastest=0.001, slowest=0.001)


def single_language_session(repo: Path, language: str = "rust") -> Session:
    return Session(repo=repo, lottery=Lottery({language: 1}), shell="bash")


async def open_result(pilot) -> ResultScreen:
    await pilot.press("s")
    await settle(pilot, ResultScreen)
    return pilot.app.screen


async def open_form(pilot) -> BootstrapScreen:
    await open_result(pilot)
    await pilot.press("b")
    await settle(pilot, BootstrapScreen)
    return pilot.app.screen


async def test_the_wheel_lists_every_language_with_its_chance(session):
    app = LotteryApp(session, timing=FAST)
    async with app.run_test() as pilot:
        table = pilot.app.screen.query_one("#wheel", DataTable)
        rows = [[str(cell) for cell in table.get_row_at(row)] for row in range(table.row_count)]
        assert rows == [
            ["python", "1", "50.0%"],
            ["rust", "1", "50.0%"],
        ]


async def test_the_numbers_are_right_aligned(session):
    app = LotteryApp(session, timing=FAST)
    async with app.run_test() as pilot:
        headers = pilot.app.screen.query_one("#wheel", DataTable).columns.values()
        assert [header.label.justify for header in headers] == [None, "right", "right"]
        cells = pilot.app.screen.query_one("#wheel", DataTable).get_row_at(0)
        assert cells[0] == "python"  # the language column is left aligned by default
        assert [cell.justify for cell in cells[1:]] == ["right", "right"]


async def test_a_draw_ends_on_the_result_screen(session):
    app = LotteryApp(session, timing=FAST)
    async with app.run_test() as pilot:
        result = await open_result(pilot)
        assert result.entry.language in {"python", "rust"}
        assert result.entry.percent == pytest.approx(50.0)


async def test_reroll_spins_again(session):
    app = LotteryApp(session, timing=FAST)
    async with app.run_test() as pilot:
        await open_result(pilot)
        await pilot.press("r")
        await settle(pilot, ResultScreen)
        assert isinstance(pilot.app.screen, ResultScreen)
        assert isinstance(pilot.app.screen_stack[-2], WheelScreen)


async def test_bootstrap_copies_the_template_and_lists_the_next_steps(repo):
    app = LotteryApp(single_language_session(repo), timing=FAST)
    async with app.run_test() as pilot:
        form = await open_form(pilot)
        form.query_one("#year", Input).value = "2026"
        form.query_one("#day", Input).value = "5"
        await pilot.pause()

        assert form.query_one("#destination", Input).value == "2026-day-05"

        form.query_one("#create", Button).press()
        await settle(pilot, NextStepsScreen)

        target = repo / "2026-day-05"
        assert pilot.app.screen.plan.destination == target
        assert (target / "src" / "main.rs").is_file()
        assert not (target / "target").exists()
        assert not (target / "input.txt").exists()


async def test_day_input_rewrites_the_destination(repo):
    app = LotteryApp(single_language_session(repo), timing=FAST)
    async with app.run_test() as pilot:
        form = await open_form(pilot)
        form.query_one("#day", Input).value = "9"
        await pilot.pause()
        assert form.query_one("#destination", Input).value.endswith("-day-09")


async def test_a_hand_edited_destination_is_kept(repo):
    app = LotteryApp(single_language_session(repo), timing=FAST)
    async with app.run_test() as pilot:
        form = await open_form(pilot)
        form.query_one("#destination", Input).value = "scratch/day-nine"
        form.query_one("#day", Input).value = "9"
        await pilot.pause()
        assert form.query_one("#destination", Input).value == "scratch/day-nine"


async def test_an_impossible_day_is_reported(repo):
    app = LotteryApp(single_language_session(repo), timing=FAST)
    async with app.run_test() as pilot:
        form = await open_form(pilot)
        form.query_one("#day", Input).value = "99"
        form.query_one("#create", Button).press()
        await pilot.pause()

        assert "day must be" in content(form.query_one("#error", Static))
        assert isinstance(pilot.app.screen, BootstrapScreen)


async def test_a_non_numeric_day_is_reported(repo):
    app = LotteryApp(single_language_session(repo), timing=FAST)
    async with app.run_test() as pilot:
        form = await open_form(pilot)
        form.query_one("#day", Input).value = "five"
        form.query_one("#create", Button).press()
        await pilot.pause()

        assert "whole number" in content(form.query_one("#error", Static))


async def test_an_existing_destination_is_reported(repo):
    (repo / "2026-day-01").mkdir(parents=True)
    app = LotteryApp(single_language_session(repo), timing=FAST)
    async with app.run_test() as pilot:
        form = await open_form(pilot)
        form.query_one("#year", Input).value = "2026"
        form.query_one("#day", Input).value = "1"
        await pilot.pause()
        form.query_one("#create", Button).press()
        await pilot.pause()

        assert "already exists" in content(form.query_one("#error", Static))


async def test_new_draw_returns_to_the_wheel(repo):
    app = LotteryApp(single_language_session(repo), timing=FAST)
    async with app.run_test() as pilot:
        form = await open_form(pilot)
        form.query_one("#day", Input).value = "5"
        form.query_one("#create", Button).press()
        await settle(pilot, NextStepsScreen)

        await pilot.press("n")
        await settle(pilot, WheelScreen)

        wheel = pilot.app.screen
        assert isinstance(wheel, WheelScreen)
        assert "Press Spin to draw" in content(wheel.query_one("#candidate", Static))


async def test_vim_keys_scroll_the_next_steps(repo):
    app = LotteryApp(single_language_session(repo), timing=FAST)
    async with app.run_test(size=(80, 24)) as pilot:
        form = await open_form(pilot)
        form.query_one("#day", Input).value = "5"
        form.query_one("#create", Button).press()
        await settle(pilot, NextStepsScreen)

        steps = pilot.app.screen.query_one(StepsView)
        await wait_until(pilot, lambda: steps.has_focus)
        assert steps.max_scroll_y > 0  # the steps are taller than the view

        await pilot.press("j")
        await pilot.pause()
        assert steps.scroll_offset.y == 1

        await pilot.press("k")
        await pilot.pause()
        assert steps.scroll_offset.y == 0

        await pilot.press("G")
        await pilot.pause()
        assert steps.scroll_offset.y == steps.max_scroll_y

        await pilot.press("g")
        await pilot.pause()
        assert steps.scroll_offset.y == 0

        await pilot.press("l")
        await pilot.press("h")
        await pilot.pause()
        assert steps.scroll_offset.y == 0


async def test_the_vim_keys_stay_out_of_the_footer():
    """The footer is left to the screen's own keys, so the scrolling keys are hidden."""
    assert not any(binding.show for binding in StepsView.BINDINGS)
    assert {binding.key for binding in StepsView.BINDINGS} == {"j", "k", "h", "l", "g", "G"}
