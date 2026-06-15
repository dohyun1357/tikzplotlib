"""Sybil configuration: execute the Python code blocks in the README so the
documented examples stay runnable. Replaces the unmaintained pytest-codeblocks.
"""

import matplotlib

# Use a non-interactive backend so README examples don't try to open windows.
matplotlib.use("Agg")

from sybil import Sybil  # noqa: E402
from sybil.parsers.markdown import PythonCodeBlockParser  # noqa: E402


def _teardown(namespace):
    # The README examples mutate global matplotlib state (e.g.
    # ``plt.style.use("ggplot")``); reset it so it can't leak into the test
    # suite when README examples run first under random ordering.
    import matplotlib.pyplot as plt

    plt.close("all")
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)


pytest_collect_file = Sybil(
    parsers=[PythonCodeBlockParser()],
    patterns=["*.md"],
    teardown=_teardown,
).pytest()
