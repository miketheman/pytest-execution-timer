# pytest-execution-timer

[![PyPI current version](https://img.shields.io/pypi/v/pytest-execution-timer.svg)](https://pypi.python.org/pypi/pytest-execution-timer)
[![Python Support](https://img.shields.io/pypi/pyversions/pytest-execution-timer.svg)](https://pypi.python.org/pypi/pytest-execution-timer)
[![Tests](https://github.com/miketheman/pytest-execution-timer/workflows/Python%20Tests/badge.svg)](https://github.com/miketheman/pytest-execution-timer/actions?query=workflow%3A%22Python+Tests%22)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/miketheman/pytest-execution-timer/main.svg)](https://results.pre-commit.ci/latest/github/miketheman/pytest-execution-timer/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A plugin to use with Pytest to measure execution time of tests.

Distinctly different from the `--durations` option of pytest,
this plugin measures specific pytest startup/collection phases.

Leverages `pytest` hooks to measure execution time of phases.

---

## Installation

Requires:

- Python 3.7 or later.
- Pytest 7.0 or later.

Install the plugin with any approach for your project.

Some examples:

```shell
pip install pytest-execution-timer
```

```shell
poetry add --dev pytest-execution-timer
```

```shell
pipenv install --dev pytest-execution-timer
```

Or add it to your `requirements.txt` file.

## Usage

Enable the plugin with the `--execution-timer` option when running `pytest`:

```console
$ pytest --execution-timer
...
Durations of pytest phases in seconds (min 100ms):
0.662	pytest_runtestloop
```

Control the threshold (default 100ms) by passing `--minimum-duration=<value in ms>`:

```console
$ pytest --execution-timer --minimum-duration=1000  # 1 second
```

## Understanding the output

The best ay to start is to compare the difference of the `pytest_runtestloop` duration
and the overall duration of the test run. Example:

```console
Durations of pytest phases in seconds (min 100ms):
0.666	pytest_runtestloop
====== 4 passed in 0.68s ======
```

In this example, there's not much lost between the test run and the `pytest_runtestloop`
meaning that the startup and collection phases are not taking too much time.

If there's a larger difference in the timings,
look to other emitted phases to understand what's taking the most time.

These can then be examined directly,
or use other tools like [profilers](https://docs.python.org/3/library/profile.html)
or [import timings](https://docs.python.org/3/using/cmdline.html#cmdoption-X).

## License

Distributed under the terms of the MIT license,
"pytest-execution-timer" is free and open source software.
See `LICENSE` for more information.
