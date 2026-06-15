# Canonical Python version (matches uv.lock's golden-reference resolution).
python_version := "3.12"
# Every supported version, and the subset that resolves the golden matplotlib.
all_versions := "3.9 3.10 3.11 3.12 3.13"
golden_versions := "3.11 3.12 3.13"
# Output-agnostic tests, safe to run where the locked matplotlib differs.
compat_tests := "README.md tests/test_cleanfigure.py tests/test_deterministic_output.py tests/test_mpl_compat.py tests/test_rotated_labels.py"

# Show available recipes.
default:
	@just --list

# Install the project and dev dependencies into .venv.
install:
	uv sync

# Other versions run in a throwaway --isolated env, so the main .venv is untouched.
# Run the test suite, optionally on another Python version (e.g. `just test 3.13`).
test python=python_version *args:
	{{ if python == python_version { "uv run" } else { "uv run --isolated --python " + python } }} --frozen pytest {{args}}

# Full suite where the locked matplotlib matches the golden refs; compat subset elsewhere.
# Run the whole version matrix, like CI.
test-all *args:
	#!/usr/bin/env bash
	set -euo pipefail
	for v in {{all_versions}}; do
	    echo "==> Python $v"
	    case " {{golden_versions}} " in *" $v "*) tests="" ;; *) tests="{{compat_tests}}" ;; esac
	    if [ "$v" = "{{python_version}}" ]; then
	        uv run --frozen pytest $tests {{args}}
	    else
	        uv run --isolated --python "$v" --frozen pytest $tests {{args}}
	    fi
	done

# Check linting and formatting.
lint:
	uv run --group lint ruff check .
	uv run --group lint ruff format --check .

# Auto-fix lint issues and format the code.
format:
	uv run --group lint ruff check --fix .
	uv run --group lint ruff format .

# Regenerate the reference .tex files (review the diff afterwards!).
refresh:
	uv run --frozen python tests/refresh_reference_files.py

# Build the HTML documentation (fails on warnings, like Read the Docs).
docs:
	uv run --group docs sphinx-build -W --keep-going -b html doc doc/_build/html

# Build the sdist and wheel.
build:
	uv build

# Remove build artifacts and caches.
clean:
	rm -rf dist build doc/_build .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

# Tag a release and publish to PyPI (run from main).
publish: build
	@test "$(git rev-parse --abbrev-ref HEAD)" = "main" || { echo "publish from main only"; exit 1; }
	gh release create "v$(uv version --short)"
	uv publish
