"""Sphinx configuration for the tikzplotlib documentation."""

import datetime
import pathlib

import tomllib

_pyproject = pathlib.Path(__file__).resolve().parent.parent / "pyproject.toml"
with open(_pyproject, "rb") as f:
    _meta = tomllib.load(f)["project"]

project = _meta["name"]
author = _meta["authors"][0]["name"]
copyright = f"2010-{datetime.date.today().year}, {author}"
release = _meta["version"]

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
exclude_patterns = ["_build"]

html_theme = "furo"
