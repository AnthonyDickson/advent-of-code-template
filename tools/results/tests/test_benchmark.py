import shutil

import pytest

from aoc_results import benchmark

SAMPLE = """Benchmark 1: ./target/release/aoc
  Time (mean ± σ):     790.4 µs ±  20.0 µs    [User: 700.0 µs, System: 90.4 µs]
  Range (min … max):   770.1 µs … 820.2 µs    10 runs

\tCommand being timed: "./target/release/aoc"
\tMaximum resident set size (kbytes): 2268
"""

needs_just = pytest.mark.skipif(shutil.which("just") is None, reason="just is required")


def test_parse_reads_the_mean_and_peak_ram():
    result = benchmark.parse(SAMPLE)
    assert result.total_us == pytest.approx(790.4)
    assert result.peak_ram_kib == 2268


@pytest.mark.parametrize(
    ("printed", "expected"),
    [
        ("5.0 ns", 0.005),
        ("12.5 µs", 12.5),
        ("250.0 us", 250.0),
        ("2.5 ms", 2500.0),
        ("1.5 s", 1_500_000.0),
    ],
)
def test_every_hyperfine_unit_converts_to_microseconds(printed, expected):
    output = f"  Time (mean ± σ):     {printed} ± 1.0 µs\nMaximum resident set size (kbytes): 10\n"
    assert benchmark.parse(output).total_us == pytest.approx(expected)


def test_missing_mean_is_reported():
    with pytest.raises(benchmark.BenchmarkError, match="mean time"):
        benchmark.parse("Maximum resident set size (kbytes): 2268\n")


def test_missing_peak_ram_is_reported():
    with pytest.raises(benchmark.BenchmarkError, match="resident set size"):
        benchmark.parse("  Time (mean ± σ):     790.4 µs ±  20.0 µs\n")


def test_a_folder_without_a_justfile_is_rejected(tmp_path):
    with pytest.raises(benchmark.BenchmarkError, match="justfile"):
        benchmark.run(tmp_path)


@needs_just
def test_run_scrapes_a_real_recipe(tmp_path):
    (tmp_path / "justfile").write_text(
        "benchmark:\n"
        "\t@printf '  Time (mean ± σ):     790.4 µs ±  20.0 µs    [User: 700.0 µs]\\n'\n"
        "\t@printf 'Maximum resident set size (kbytes): 2268\\n'\n",
        encoding="utf-8",
    )
    result = benchmark.run(tmp_path)
    assert result.total_us == pytest.approx(790.4)
    assert result.peak_ram_kib == 2268


@needs_just
def test_a_failing_recipe_is_reported(tmp_path):
    (tmp_path / "justfile").write_text("benchmark:\n\t@exit 3\n", encoding="utf-8")
    with pytest.raises(benchmark.BenchmarkError, match="failed"):
        benchmark.run(tmp_path)
