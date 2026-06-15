# Python version the locked environment and golden references target.
python_version := "3.12"

# Show available recipes.
default:
	@just --list

# Install the project and dev dependencies into .venv.
install:
	uv sync

# Run the test suite (optionally on another Python version, e.g. `just test 3.13`).
# Other versions run in a throwaway --isolated env, so the main .venv is untouched.
test python=python_version *args:
	{{ if python == python_version { "uv run" } else { "uv run --isolated --python " + python } }} --frozen pytest {{args}}

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
