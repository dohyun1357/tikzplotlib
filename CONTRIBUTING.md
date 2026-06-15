# Contributing

This project uses [uv](https://docs.astral.sh/uv/) for environment and
dependency management.

## Development setup

```sh
uv sync            # create .venv and install the project + dev dependencies
uv run pytest      # run the test suite
```

Common tasks are wrapped in the [`justfile`](justfile):

```sh
just test          # run the full test suite (Python 3.12)
just test 3.13     # run it on another Python version
just lint          # ruff check + ruff format --check
just format        # ruff check --fix + ruff format
just refresh       # regenerate the reference .tex files (see below)
just docs          # build the docs (strict, like Read the Docs)
```

The suite includes byte-for-byte golden references that target the Python 3.12
dependency resolution in `uv.lock`, so `just test` defaults to 3.12. Other Python
versions may resolve a different matplotlib and produce legitimate output
differences in the golden tests; CI covers them with an output-agnostic
compatibility matrix (see below).

Linting/formatting is handled entirely by [ruff](https://docs.astral.sh/ruff/),
also wired up as a pre-commit hook (`pre-commit install`).

## Isolating matplotlib's volatile API

matplotlib regularly renames or removes the private attributes/helpers this
project relies on. **Keep all such version-sensitive access in
[`src/tikzplotlib/_mpl_compat.py`](src/tikzplotlib/_mpl_compat.py)** behind a
small accessor that prefers a public API and falls back to the private one. That
way a future matplotlib change only touches one file. Avoid reaching into
matplotlib internals (`obj._something`) directly from the rest of the code.

## The golden reference tests

Most tests compare generated TikZ output byte-for-byte against the
`tests/*_reference.tex` files. Those references correspond to the Python 3.12
dependency resolution pinned in `uv.lock`. CI runs these golden tests only in
that canonical environment, so the references change only deliberately.

When you intentionally change the output (or bump matplotlib):

```sh
uv lock --upgrade-package matplotlib   # (only when bumping matplotlib)
uv sync
just refresh                           # regenerate the references
git diff tests/                        # review every change!
```

Review the diff carefully: each change should be an explainable consequence of
your change or of a matplotlib default change — **not** a malformed-TikZ
regression. `refresh` skips a few tests with non-standard structure
(`test_rotated_labels`, `test_deterministic_output`, `test_cleanfigure`,
`test_context`); update those by hand if needed.

Prefer assertions that are robust to matplotlib's formatting (e.g. asserting the
number of points removed by `clean_figure`, not absolute line counts).

## CI

- The **golden** job runs the full suite, including byte-for-byte reference
  comparisons, against the canonical locked Python 3.12 environment on Linux.
- The **compatibility** matrix runs output-agnostic README, `clean_figure`,
  focused Matplotlib compatibility, deterministic-output, and rotated-label
  tests against the locked dependencies on Python 3.9–3.13 across
  Linux/macOS/Windows.
- The **smoke-latest** job (also weekly via cron) runs the output-agnostic
  README examples against the newest matplotlib/numpy to catch upstream API
  breakage early, separately from cosmetic output drift.
