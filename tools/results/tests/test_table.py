from pathlib import Path

import pytest

from aoc_results import repository, table


def test_microseconds_are_rounded_and_grouped():
    assert table.format_microseconds(790.4) == "790 µs"
    assert table.format_microseconds(143000.0) == "143,000 µs"
    assert table.format_microseconds(0.4) == "0 µs"


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("fsharp", "F#"),
        ("common-lisp", "Common Lisp"),
        ("ocaml", "OCaml"),
        ("cobol", "Cobol"),
        ("some-new-lang", "Some New Lang"),
    ],
)
def test_language_labels_use_the_display_name(language, expected):
    assert table.language_label(language) == expected


def test_a_vendored_icon_becomes_a_markdown_image():
    assert table.language_label("rust", "tools/results/icons") == (
        "![Rust](tools/results/icons/rust.svg)"
    )


def test_languages_without_an_icon_fall_back_to_their_name():
    assert table.language_label("prolog", "tools/results/icons") == "Prolog"
    assert table.language_label("shakespeare", "tools/results/icons") == "Shakespeare"


def test_every_named_icon_file_exists_in_the_icon_directory():
    for filename in table.LANGUAGE_ICONS.values():
        assert (table.ICON_DIR / filename).is_file(), filename


def test_every_template_has_a_display_name():
    root = repository.discover()
    for language in repository.languages(root):
        assert language in table.LANGUAGE_NAMES


def test_the_icon_prefix_is_relative_to_the_results_file(tmp_path):
    prefix = table.relative_icon_prefix(tmp_path / "RESULTS.md")
    assert Path(prefix).name == "icons"
    assert not Path(prefix).is_absolute()


def test_rows_read_the_solution_time_as_the_difference():
    row = table.Row(
        language="rust",
        day=1,
        part="Both",
        baseline_us=718.0,
        total_us=790.0,
        peak_ram_kib=2268,
        lines=57,
    )
    assert row.solution_us == pytest.approx(72.0)
    assert row.cells() == ["1 (Both)", "Rust", "718 µs", "790 µs", "72 µs", "2,268", "57"]
    assert row.cells("tools/results/icons")[1] == "![Rust](tools/results/icons/rust.svg)"


def test_a_total_below_the_baseline_never_goes_negative():
    row = table.Row(
        language="rust",
        day=1,
        part="Both",
        baseline_us=900.0,
        total_us=790.0,
        peak_ram_kib=2268,
        lines=57,
    )
    assert row.solution_us == 0.0


def test_upsert_creates_the_file_with_a_header_and_a_row(tmp_path):
    path = tmp_path / "RESULTS.md"
    table.upsert(path, _row(day=1, part="Both"))

    document = path.read_text(encoding="utf-8")
    assert document.startswith("# Results\n")
    assert (
        "| Day (Part) | Language | Baseline Time | Total Time | Solution Time | Peak RAM (KiB) | Lines |"
        in document
    )
    assert "| :--- | :--- | ---: | ---: | ---: | ---: | ---: |" in document  # the alignment row
    assert "| 1 (Both) | Rust | 718 µs | 790 µs | 72 µs | 2,268 | 57 |" in document
    assert "| 🦀 Rust" not in document


def test_upsert_links_the_vendored_icon_when_given_a_prefix(tmp_path):
    path = tmp_path / "RESULTS.md"
    table.upsert(path, _row(day=1, part="Both"), icon_prefix="tools/results/icons")

    assert "![Rust](tools/results/icons/rust.svg)" in path.read_text(encoding="utf-8")


def test_upsert_replaces_the_row_for_the_same_day_and_part(tmp_path):
    path = tmp_path / "RESULTS.md"
    table.upsert(path, _row(day=5, part="1", total_us=1000.0))
    table.upsert(path, _row(day=5, part="1", total_us=5000.0))

    rows = _rows(path)
    assert len(rows) == 1
    assert "5,000 µs" in rows[0]


def test_upsert_sorts_by_day_then_part(tmp_path):
    path = tmp_path / "RESULTS.md"
    table.upsert(path, _row(day=3, part="Both"))
    table.upsert(path, _row(day=1, part="Both"))
    table.upsert(path, _row(day=1, part="1"))
    table.upsert(path, _row(day=1, part="2"))

    assert [row.split("|")[1].strip() for row in _rows(path)] == [
        "1 (1)",
        "1 (2)",
        "1 (Both)",
        "3 (Both)",
    ]


def test_upsert_keeps_a_hand_written_preamble_and_other_rows(tmp_path):
    path = tmp_path / "RESULTS.md"
    path.write_text(
        "# My results\n\nRecorded by hand.\n\n"
        "| Day (Part) | Language | Baseline Time | Total Time | Solution Time | Peak RAM (KiB) |\n"
        "| :--------- | :------- | ------------: | ---------: | ------------: | -------------: |\n"
        "| 2 (1)      | ✨ Magic |       100 µs  |     200 µs |        100 µs |            128 |\n",
        encoding="utf-8",
    )
    table.upsert(path, _row(day=1, part="Both"))

    document = path.read_text(encoding="utf-8")
    assert document.startswith("# My results\n\nRecorded by hand.")
    rows = _rows(path)
    assert len(rows) == 2
    assert "2 (1)" in rows[1]
    assert "1 (Both)" in rows[0]


def _row(*, day: int, part: str, total_us: float = 790.0) -> table.Row:
    return table.Row(
        language="rust",
        day=day,
        part=part,
        baseline_us=718.0,
        total_us=total_us,
        peak_ram_kib=2268,
        lines=57,
    )


def _rows(path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if line.lstrip().startswith("|")][2:]
