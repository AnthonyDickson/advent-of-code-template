"""Textual TUI: spin the wheel, then bootstrap the day's solution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, cast

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Input, Label, Markdown, Static

from aoc_lottery.bootstrap import (
    LAST_DAY,
    Bootstrap,
    BootstrapError,
    bootstrap,
    current_year,
    default_destination,
    display_path,
)
from aoc_lottery.guidance import next_steps_markdown
from aoc_lottery.lottery import Entry
from aoc_lottery.session import Session


@dataclass(frozen=True)
class SpinTiming:
    """Seconds between the highlighted language moving during a spin."""

    fastest: float = 0.03
    slowest: float = 0.24


class LotteryApp(App[None]):
    """The language lottery."""

    TITLE = "Advent of Code language lottery"
    SUB_TITLE = "Weighted draw from template/"
    BINDINGS: ClassVar[list[BindingType]] = [("q", "quit_app", "Quit")]
    CSS = """
    Screen {
        padding: 1 2;
    }

    .heading {
        width: 100%;
        text-align: center;
        text-style: bold;
        color: $accent;
    }

    .subheading {
        width: 100%;
        text-align: center;
        color: $text-muted;
    }

    #wheel {
        height: 1fr;
        margin: 1 0;
        border: round $primary;
    }

    #candidate {
        height: 3;
        width: 100%;
        content-align: center middle;
        text-style: bold;
    }

    #winner {
        height: 3;
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $success;
    }

    #buttons {
        height: auto;
        width: 100%;
        align-horizontal: center;
    }

    #buttons Button {
        margin: 0 1;
    }

    .field-label {
        color: $text-muted;
        margin-top: 1;
    }

    #destination {
        margin-bottom: 1;
    }

    #error {
        height: auto;
        color: $error;
    }

    #steps {
        height: 1fr;
        margin: 1 0;
        padding: 0 1;
        border: round $primary;
    }
    """

    def __init__(self, session: Session, *, timing: SpinTiming | None = None) -> None:
        super().__init__()
        self.session = session
        self.timing = timing or SpinTiming()

    def on_mount(self) -> None:
        self.push_screen(WheelScreen(self.session))

    def action_quit_app(self) -> None:
        self.exit()


class LotteryScreen(Screen[None]):
    """Base screen holding the shared session."""

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    @property
    def lottery_app(self) -> LotteryApp:
        return cast("LotteryApp", self.app)

    def quit_app(self) -> None:
        self.lottery_app.exit()

    def new_draw(self) -> None:
        """Return to the wheel the session started with, clearing every screen on top of it."""
        app = self.lottery_app
        wheel = next(
            (screen for screen in app.screen_stack if isinstance(screen, WheelScreen)), None
        )
        if wheel is None:
            app.push_screen(WheelScreen(self.session))
            return
        while app.screen is not wheel:
            app.pop_screen()
        wheel.reset()


class WheelScreen(LotteryScreen):
    """Shows every language and its weight, then spins through them."""

    BINDINGS: ClassVar[list[BindingType]] = [("s", "spin", "Spin")]

    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self._order: tuple[str, ...] = ()
        self._row = 0
        self._remaining = 0
        self._total = 0
        self._winner: Entry | None = None
        self._spinning = False

    @property
    def timing(self) -> SpinTiming:
        return self.lottery_app.timing

    def compose(self) -> ComposeResult:
        yield Static("Language lottery", classes="heading")
        yield Static(
            "Weighted draw from template/. Re-roll until you like the pick.", classes="subheading"
        )
        yield DataTable(id="wheel", zebra_stripes=True)
        yield Static("Press Spin to draw", id="candidate")
        with Horizontal(id="buttons"):
            yield Button("Spin", id="spin", variant="primary")
            yield Button("Quit", id="quit")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#wheel", DataTable)
        table.cursor_type = "row"
        # The numbers are aligned right so the weights and chances line up under their headings.
        table.add_columns("Language", _right("Weight"), _right("Chance"))
        for entry in self.session.lottery.entries:
            table.add_row(
                entry.language,
                _right(f"{entry.weight:g}"),
                _right(f"{entry.percent:.1f}%"),
                key=entry.language,
            )
        table.move_cursor(row=0)
        self._order = tuple(entry.language for entry in self.session.lottery.entries)
        self.query_one("#spin", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "spin":
            self.action_spin()
        elif event.button.id == "quit":
            self.quit_app()

    def reset(self) -> None:
        """Put the wheel back to how it looked before the first spin."""
        self._spinning = False
        self._winner = None
        self._row = 0
        self.query_one("#spin", Button).disabled = False
        self.query_one("#candidate", Static).update("Press Spin to draw")
        self.query_one("#wheel", DataTable).move_cursor(row=0)
        self.query_one("#spin", Button).focus()

    def action_spin(self) -> None:
        """Draw a winner and animate the wheel towards it."""
        if self._spinning or not self._order:
            return
        self._spinning = True
        self.query_one("#spin", Button).disabled = True
        self._winner = self.session.lottery.draw()

        target = self.session.lottery.row_of(self._winner.language)
        self._total = (target - self._row) % len(self._order) + 2 * len(self._order)
        self._remaining = self._total
        self._advance()

    def _advance(self) -> None:
        self._remaining -= 1
        self._row = (self._row + 1) % len(self._order)
        self._highlight(self._order[self._row])
        if self._remaining <= 0:
            self.set_timer(self.timing.slowest, self._land)
            return
        progress = 1 - self._remaining / self._total
        delay = self.timing.fastest + (self.timing.slowest - self.timing.fastest) * progress**2
        self.set_timer(delay, self._advance)

    def _highlight(self, language: str) -> None:
        self.query_one("#wheel", DataTable).move_cursor(row=self.session.lottery.row_of(language))
        self.query_one("#candidate", Static).update(language)

    def _land(self) -> None:
        self._spinning = False
        winner = cast("Entry", self._winner)
        self.query_one("#candidate", Static).update(winner.language)
        self.lottery_app.push_screen(ResultScreen(self.session, winner))


class ResultScreen(LotteryScreen):
    """The drawn language, with the option to re-roll or bootstrap it."""

    BINDINGS: ClassVar[list[BindingType]] = [
        ("r", "reroll", "Re-roll"),
        ("b", "bootstrap", "Bootstrap"),
    ]

    def __init__(self, session: Session, entry: Entry) -> None:
        super().__init__(session)
        self.entry = entry

    def compose(self) -> ComposeResult:
        yield Static("The wheel has spoken", classes="heading")
        yield Static(self.entry.language, id="winner")
        yield Static(
            f"weight {self.entry.weight:g}, {self.entry.percent:.1f}% chance", classes="subheading"
        )
        with Horizontal(id="buttons"):
            yield Button("Bootstrap a day", id="bootstrap", variant="primary")
            yield Button("Re-roll", id="reroll")
            yield Button("Quit", id="quit")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "bootstrap":
            self.action_bootstrap()
        elif event.button.id == "reroll":
            self.action_reroll()
        elif event.button.id == "quit":
            self.quit_app()

    def action_bootstrap(self) -> None:
        self.lottery_app.push_screen(BootstrapScreen(self.session, self.entry))

    def action_reroll(self) -> None:
        self.lottery_app.pop_screen()
        wheel = self.lottery_app.screen
        if isinstance(wheel, WheelScreen):
            wheel.action_spin()


class BootstrapScreen(LotteryScreen):
    """Ask for the day, then copy the template."""

    def __init__(self, session: Session, entry: Entry) -> None:
        super().__init__(session)
        self.entry = entry
        self._auto_destination = self._default_destination(current_year(), 1)

    def compose(self) -> ComposeResult:
        yield Static(f"Bootstrap {self.entry.language}", classes="heading")
        yield Static(
            "Which day is this? The template is copied into a new folder.", classes="subheading"
        )
        yield Label("Year", classes="field-label")
        yield Input(value=str(current_year()), id="year")
        yield Label(f"Day (1-{LAST_DAY})", classes="field-label")
        yield Input(placeholder="e.g. 5", id="day")
        yield Label("Destination", classes="field-label")
        yield Input(value=self._auto_destination, id="destination")
        yield Static("", id="error")
        with Horizontal(id="buttons"):
            yield Button("Copy template", id="create", variant="primary")
            yield Button("Back", id="back")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#day", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create":
            self.create()
        elif event.button.id == "back":
            self.lottery_app.pop_screen()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "destination":
            self.create()
        else:
            self.query_one("#destination", Input).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Keep the destination in step with the year and day until it is edited by hand."""
        if event.input.id not in {"year", "day"}:
            return
        if self.query_one("#destination", Input).value != self._auto_destination:
            return
        self._auto_destination = self._current_destination()
        self.query_one("#destination", Input).value = self._auto_destination

    def create(self) -> None:
        """Copy the template, or explain why it cannot be copied yet."""
        error = self.query_one("#error", Static)
        error.update("")
        try:
            year = _parse_int(self.query_one("#year", Input).value, "year")
            day = _parse_int(self.query_one("#day", Input).value, "day")
        except ValueError as problem:
            error.update(str(problem))
            return

        destination = self.query_one("#destination", Input).value.strip()
        try:
            plan = bootstrap(self.session.repo, self.entry.language, year, day, destination or None)
        except BootstrapError as problem:
            error.update(str(problem))
            return

        self.lottery_app.push_screen(NextStepsScreen(self.session, plan))

    def _current_destination(self) -> str:
        year = _parse_int(self.query_one("#year", Input).value, "year", fallback=current_year())
        day = _parse_int(self.query_one("#day", Input).value, "day", fallback=1)
        return self._default_destination(year, day)

    def _default_destination(self, year: int, day: int) -> str:
        clamped = max(1, min(day, LAST_DAY))
        path = default_destination(self.session.repo, year, clamped)
        return display_path(path, self.session.repo)


class StepsView(ScrollableContainer):
    """The next steps, scrollable with the arrow keys, j/k/h/l and g/G.

    These bindings are hidden from the footer, which only has room for the screen's own keys; the
    keys are documented in the tool's README instead.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("j", "line_down", "Down", show=False),
        Binding("k", "line_up", "Up", show=False),
        Binding("h", "line_left", "Left", show=False),
        Binding("l", "line_right", "Right", show=False),
        Binding("g", "jump_top", "Top", show=False),
        Binding("G", "jump_bottom", "Bottom", show=False),
    ]

    def action_line_down(self) -> None:
        self.scroll_down(animate=False)

    def action_line_up(self) -> None:
        self.scroll_up(animate=False)

    def action_line_left(self) -> None:
        self.scroll_left(animate=False)

    def action_line_right(self) -> None:
        self.scroll_right(animate=False)

    def action_jump_top(self) -> None:
        self.scroll_home(animate=False)

    def action_jump_bottom(self) -> None:
        self.scroll_end(animate=False)


class NextStepsScreen(LotteryScreen):
    """The copy is done: show what is left to do."""

    BINDINGS: ClassVar[list[BindingType]] = [("n", "new_draw", "New draw")]
    # Focus the steps so j/k/h/l and the arrow keys scroll them straight away.
    AUTO_FOCUS = "#steps"

    def __init__(self, session: Session, plan: Bootstrap) -> None:
        super().__init__(session)
        self.plan = plan

    def compose(self) -> ComposeResult:
        yield Static(f"{self.plan.language} bootstrapped", classes="heading")
        yield Static(
            f"{display_path(self.plan.source, self.session.repo)} to "
            f"{display_path(self.plan.destination, self.session.repo)} "
            f"({self.plan.file_count} files)",
            classes="subheading",
        )
        with StepsView(id="steps"):
            yield Markdown(next_steps_markdown(self.plan, self.session.repo, self.session.shell))
        with Horizontal(id="buttons"):
            yield Button("New draw", id="again", variant="primary")
            yield Button("Quit", id="quit")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "again":
            self.new_draw()
        elif event.button.id == "quit":
            self.quit_app()

    def action_new_draw(self) -> None:
        self.new_draw()


def _right(text: str) -> Text:
    """A table cell aligned to the right, for the weight and chance columns."""
    return Text(text, justify="right")


def _parse_int(text: str, label: str, fallback: int | None = None) -> int:
    try:
        return int(text.strip())
    except ValueError:
        if fallback is not None:
            return fallback
        raise ValueError(f"{label} must be a whole number") from None
