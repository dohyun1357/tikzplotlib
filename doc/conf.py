# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import datetime
import pathlib

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# Sphinx 1.* compat (for readthedocs)
master_doc = "index"

this_dir = pathlib.Path(__file__).resolve().parent
with open(this_dir / ".." / "pyproject.toml", "rb") as f:
    p = tomllib.load(f)["project"]

# -- Project information -----------------------------------------------------
project = p["name"]
year = datetime.datetime.utcnow().year
author = p["authors"][0]["name"]
copyright = f"2010-{year}, {author}"

release = p["version"]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

html_theme_options = {
    # "logo": "meshplex-logo.svg",
    "github_user": "nschloe",
    "github_repo": "tikzplotlib",
    "github_banner": True,
    "github_button": False,
}
