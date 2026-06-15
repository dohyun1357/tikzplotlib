version := `uv version --short`

default:
	@echo "\"just publish\"?"

publish:
	@if [ "$(git rev-parse --abbrev-ref HEAD)" != "main" ]; then exit 1; fi
	gh release create "v{{version}}"
	rm -rf dist/
	uv build
	uv publish

clean:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
	@rm -rf src/*.egg-info/ build/ dist/ .tox/ ./doc/_build/

format:
	uv run --group lint ruff check --fix .
	uv run --group lint ruff format .

lint:
	uv run --group lint ruff check .
	uv run --group lint ruff format --check .

test *args:
	uv run pytest {{args}}

refresh:
	uv run python tests/refresh_reference_files.py
