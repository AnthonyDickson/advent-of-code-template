import pytest

from aoc_results import benchmark
from aoc_results.__main__ import main


def test_records_a_row_with_a_given_baseline(repo, solution, monkeypatch, capsys):
    monkeypatch.setattr(benchmark, "run", lambda directory: benchmark.Benchmark(790.0, 2268))

    exit_code = main(["--repo", str(repo), "--baseline", "500", str(solution)])

    assert exit_code == 0
    document = (repo / "RESULTS.md").read_text(encoding="utf-8")
    assert "| 5 (Both)" in document
    assert "![Rust]" in document
    assert "rust.svg)" in document
    assert "500 µs" in document
    assert "290 µs" in document
    assert "2,268" in document
    assert "recorded in" in capsys.readouterr().out


def test_measures_the_template_baseline_on_the_input(repo, solution, monkeypatch):
    calls = []

    def fake_run(directory):
        calls.append(directory)
        if len(calls) == 1:
            return benchmark.Benchmark(5000.0, 9000)
        return benchmark.Benchmark(1000.0, 4000)

    monkeypatch.setattr(benchmark, "run", fake_run)

    exit_code = main(["--repo", str(repo), str(solution)])

    assert exit_code == 0
    assert calls[0] == solution
    assert calls[1] == repo / "template" / "rust"  # the baseline is benchmarked in the template
    document = (repo / "RESULTS.md").read_text(encoding="utf-8")
    assert "1,000 µs" in document  # baseline column
    assert "4,000 µs" in document  # solution time column


def test_a_failed_benchmark_is_reported(repo, solution, monkeypatch, capsys):
    def explode(directory):
        raise benchmark.BenchmarkError("`just benchmark` failed")

    monkeypatch.setattr(benchmark, "run", explode)

    exit_code = main(["--repo", str(repo), "--baseline", "500", str(solution)])

    assert exit_code == 1
    assert "error:" in capsys.readouterr().err
    assert not (repo / "RESULTS.md").exists()


def test_a_missing_folder_is_reported(repo, capsys):
    exit_code = main(["--repo", str(repo), str(repo / "2026-day-09")])

    assert exit_code == 1
    assert "error:" in capsys.readouterr().err


@pytest.mark.parametrize(("part", "label"), [("1", "1"), ("2", "2"), ("both", "Both")])
def test_each_part_gets_its_own_label(repo, solution, monkeypatch, part, label):
    monkeypatch.setattr(benchmark, "run", lambda directory: benchmark.Benchmark(790.0, 2268))

    exit_code = main(
        ["--repo", str(repo), "--baseline", "500", "--day", "7", "--part", part, str(solution)]
    )

    assert exit_code == 0
    assert f"7 ({label})" in (repo / "RESULTS.md").read_text(encoding="utf-8")
