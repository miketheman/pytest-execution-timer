import pytest


def test_shows_help_when_enabled(pytester):
    result = pytester.runpytest("--help")
    assert result.ret == 0
    result.stdout.fnmatch_lines(
        ["*execution_timer:*", "*--execution-timer*", "*--minimum-duration*"]
    )


def test_does_not_emit_when_not_enabled(pytester):
    pytester.makepyfile(
        """
        import time

        def test_execution():
            time.sleep(0.2)
        """
    )
    result = pytester.runpytest()
    assert result.ret == 0
    # Confirm that the plugin output is not present
    with pytest.raises(pytest.fail.Exception):
        result.stdout.fnmatch_lines(["*Durations*", "*0.*pytest_runtestloop*"])


def test_omits_duration_when_enabled(pytester):
    pytester.makepyfile(
        """
        import time

        def test_execution():
            time.sleep(0.2)
        """
    )
    result = pytester.runpytest("--execution-timer")
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*Durations*", "*0.*pytest_runtestloop*"])


def test_configured_duration_is_used(pytester):
    pytester.makepyfile(
        """
        import time

        def test_execution():
            time.sleep(0.1)
        """
    )
    result = pytester.runpytest("--execution-timer", "--minimum-duration=100")
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*Durations*", "*0.*pytest_runtestloop*"])
