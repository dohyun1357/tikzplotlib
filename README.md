# tikzplotlib

[![PyPI version](https://img.shields.io/pypi/v/tikzplotlib.svg?style=flat-square)](https://pypi.org/project/tikzplotlib/)
[![Python versions](https://img.shields.io/pypi/pyversions/tikzplotlib.svg?style=flat-square)](https://pypi.org/project/tikzplotlib/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

Convert [matplotlib](https://matplotlib.org/) figures into
[PGFPlots](https://www.ctan.org/pkg/pgfplots)
([PGF/TikZ](https://www.ctan.org/pkg/pgf)) code for native inclusion in LaTeX or
ConTeXt documents.

Unlike matplotlib's raw PGF backend, PGFPlots describes a graph in terms of axes
and data rather than low-level drawing commands, so the output retains more
information and is much easier to read and tweak by hand.

## Installation

```sh
pip install tikzplotlib
# or
uv add tikzplotlib
```

## Usage

Build a figure with matplotlib as usual, then hand it to tikzplotlib:

```python
import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0.0, 2.0, 0.1)
plt.plot(t, np.sin(2 * np.pi * t), "o-")
plt.xlabel("time (s)")

import tikzplotlib

tikzplotlib.save("plot.tex")
```

- `tikzplotlib.get_tikz_code()` returns the code as a string instead of writing a file.
- Pass `flavor="context"` for ConTeXt output.
- `tikzplotlib.clean_figure()` (call it before saving) drops points outside the
  axes, simplifies lines, and reduces point density.

Include the result with `\input{plot.tex}` and add the required packages to your
preamble:

```latex
\usepackage{pgfplots}
\DeclareUnicodeCharacter{2212}{−}
\usepgfplotslibrary{groupplots,dateplot}
\usetikzlibrary{patterns,shapes.arrows}
\pgfplotsset{compat=newest}
```

`tikzplotlib.Flavors.latex.preamble()` (or `.context`) returns this snippet
programmatically.

## Documentation

The API reference is hosted on [Read the Docs](https://tikzplotlib.readthedocs.io/).

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for the
development setup and workflow.

## License

tikzplotlib is licensed under the [MIT License](LICENSE).
