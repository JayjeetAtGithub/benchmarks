import pytest

from .. import _sources
from .. import dataframe_to_table_benchmark
from ..tests._asserts import assert_benchmark, assert_cli, R_CLI


HELP = """
Usage: conbench dataframe-to-table [OPTIONS] SOURCE

  Run dataframe-to-table benchmark.

Options:
  --language [Python|R]
  --cpu-count INTEGER
  --iterations INTEGER   [default: 1]
  --drop-caches BOOLEAN  [default: False]
  --gc-collect BOOLEAN   [default: True]
  --gc-disable BOOLEAN   [default: True]
  --show-result BOOLEAN  [default: True]
  --show-output BOOLEAN  [default: False]
  --run-id TEXT          Group executions together with a run id.
  --run-name TEXT        Name of run (commit, pull request, etc).
  --help                 Show this message and exit.
"""


def assert_run(run, index, benchmark, source):
    result, output = run[index]
    assert_benchmark(result, source.name, benchmark.name)
    assert "pyarrow.Table" in str(output)


def assert_run_r(run, index, benchmark, source):
    result, output = run[index]
    assert_benchmark(result, source.name, benchmark.name, language="R")
    assert R_CLI in str(output)


@pytest.mark.slow
def test_dataframe_to_table():
    benchmark = dataframe_to_table_benchmark.DataframeToTableBenchmark()
    sources = [_sources.Source(s) for s in benchmark.sources_test]
    run = list(benchmark.run(sources, iterations=1))
    assert len(run) == 7
    for x in range(len(run)):
        assert_run(run, x, benchmark, sources[x])


@pytest.mark.slow
def test_dataframe_to_table_r():
    benchmark = dataframe_to_table_benchmark.DataframeToTableBenchmark()
    sources = [_sources.Source(s) for s in benchmark.sources_test]
    run = list(benchmark.run(sources, language="R"))
    assert len(run) == 7
    for x in range(len(run)):
        assert_run(run, x, benchmark, sources[x])


def test_dataframe_to_table_cli():
    command = ["conbench", "dataframe-to-table", "--help"]
    assert_cli(command, HELP)
