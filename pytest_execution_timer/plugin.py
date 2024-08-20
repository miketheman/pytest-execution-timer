import time
import typing
from datetime import timedelta

import pytest


class PytestExecutionTimer:
    """
    A timer for the phases of Pytest's execution.
    Distinctly different from `--durations=N`
    in that this reports times spent **outside** tests.

    Not every hook is instrumented yet,
    only the ones that I've observed causing slowdown.
    More hook contributions are welcome!
    """

    durations: typing.Dict[str, float] = dict()

    # === Initialization Hooks ===
    # https://docs.pytest.org/en/stable/reference.html#initialization-hooks
    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_sessionstart(self, session):
        start = time.time()
        yield
        end = time.time()
        self.durations["pytest_sessionstart"] = end - start

    # === Collection Hooks ===
    # https://docs.pytest.org/en/stable/reference.html#collection-hooks
    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_collection(self, session):
        start = time.time()
        yield
        end = time.time()
        self.durations["pytest_collection"] = end - start

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_collect_file(self, path, parent):
        start = time.time()
        yield
        end = time.time()
        self.durations[f"pytest_collect_file:{path}"] = end - start

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_itemcollected(self, item):
        start = time.time()
        yield
        end = time.time()
        self.durations[f"pytest_itemcollected\t{item.name}"] = end - start

    # === Run Test Hooks ===
    # https://docs.pytest.org/en/stable/reference.html#test-running-runtest-hooks
    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtestloop(self, session):
        """Should mimic the output of the total test time reported by pytest.
        May not be necessary."""
        start = time.time()
        yield
        end = time.time()
        self.durations["pytest_runtestloop"] = end - start

    # === Reporting Hooks ===
    # https://docs.pytest.org/en/stable/reference.html#reporting-hooks
    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_make_collect_report(self, collector):
        """Despite being a Reporting hook, this fires during the Collection phase
        and can find `test_*.py` level import slowdowns."""
        start = time.time()
        yield
        end = time.time()
        self.durations[f"pytest_make_collect_report\t{collector.nodeid}"] = end - start

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        """Where we emit our report."""
        min_duration = config.option.minimum_duration_in_ms

        terminalreporter.section("pytest-execution-timer")
        terminalreporter.write_line(
            f"Durations of pytest phases in seconds (min {min_duration}ms):"
        )

        for key, value in self.durations.items():
            # Only show items that took longer than the configured value
            if value > timedelta(milliseconds=min_duration).total_seconds():
                terminalreporter.write_line(f"{value:.3f}\t{key}")


def pytest_addoption(parser):
    group = parser.getgroup("execution_timer")
    group.addoption(
        "--execution-timer",
        action="store_true",
        dest="execution_timer",
        help="Enable collection of pytest phase execution timing.",
    )
    group.addoption(
        "--minimum-duration",
        action="store",
        dest="minimum_duration_in_ms",
        type=int,
        default=100,
        help="Minimum duration in milliseconds to show in the report.",
    )


def pytest_configure(config):
    if config.option.execution_timer:
        config.pluginmanager.register(PytestExecutionTimer())
