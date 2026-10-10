import json
import shutil

import pytest

from aoc_results import benchmark


def export(mean=0.0007904, memory=(2_322_432, 2_318_336)):
    """A hyperfine ``--export-json`` document with one command's results."""
    return json.dumps(
        {
            "results": [
                {
                    "command": "./target/release/aoc",
                    "mean": mean,
                    "stddev": 0.00002,
                    "times": [mean] * len(memory),
                    "memory_usage_byte": list(memory),
                    "exit_codes": [0] * len(memory),
                }
            ]
        }
    )


needs_just = pytest.mark.skipif(shutil.which("just") is None, reason="just is required")


def test_parse_reads_the_mean_and_peak_ram():
    result = benchmark.parse(export())
    assert result.total_us == pytest.approx(790.4)
    assert result.peak_ram_kib == 2268


def test_parse_takes_the_largest_run_as_the_peak():
    result = benchmark.parse(export(memory=(1024, 4096, 2048)))
    assert result.peak_ram_kib == 4


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0.000000005, 0.005),
        (0.0000125, 12.5),
        (0.0025, 2500.0),
        (1.5, 1_500_000.0),
    ],
)
def test_seconds_convert_to_microseconds(seconds, expected):
    assert benchmark.parse(export(mean=seconds)).total_us == pytest.approx(expected)


@pytest.mark.parametrize(
    "document",
    [
        "not json",
        json.dumps({"results": []}),
        json.dumps({"results": [{"memory_usage_byte": [1024]}]}),
        json.dumps({"results": [{"mean": 0.1}]}),
        json.dumps({"results": [{"mean": 0.1, "memory_usage_byte": []}]}),
    ],
)
def test_an_unreadable_export_is_reported(document):
    with pytest.raises(benchmark.BenchmarkError, match="JSON export"):
        benchmark.parse(document)


def test_a_folder_without_a_justfile_is_rejected(tmp_path):
    with pytest.raises(benchmark.BenchmarkError, match="justfile"):
        benchmark.run(tmp_path)


@needs_just
def test_run_reads_the_export_a_real_recipe_writes(tmp_path):
    (tmp_path / "export.json").write_text(export(), encoding="utf-8")
    (tmp_path / "justfile").write_text(
        "benchmark flag path:\n\t@cp export.json {{path}}\n",
        encoding="utf-8",
    )
    result = benchmark.run(tmp_path)
    assert result.total_us == pytest.approx(790.4)
    assert result.peak_ram_kib == 2268


@needs_just
def test_a_recipe_that_ignores_its_arguments_is_reported(tmp_path):
    (tmp_path / "justfile").write_text("benchmark *args:\n\t@true\n", encoding="utf-8")
    with pytest.raises(benchmark.BenchmarkError, match="no hyperfine JSON"):
        benchmark.run(tmp_path)


@needs_just
def test_a_failing_recipe_is_reported(tmp_path):
    (tmp_path / "justfile").write_text("benchmark *args:\n\t@exit 3\n", encoding="utf-8")
    with pytest.raises(benchmark.BenchmarkError, match="failed"):
        benchmark.run(tmp_path)
