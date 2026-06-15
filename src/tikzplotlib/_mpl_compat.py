"""Compatibility shims isolating tikzplotlib from matplotlib's volatile APIs.

matplotlib regularly renames or removes the private attributes and helpers that
tikzplotlib relies on. Keep *all* such version-sensitive access in this single
module: each accessor prefers a public API and falls back to private attributes
behind a guard, so a future matplotlib change touches only this file.
"""

import functools
import re

import matplotlib as mpl

# ---------------------------------------------------------------------------
# Text escaping
# ---------------------------------------------------------------------------
# Vendored from matplotlib 3.5.1's ``backend_pgf.common_texification``. That
# function was later renamed to the private ``_tex_escape`` and reduced to only
# replacing the unicode minus sign, but tikzplotlib needs the original escaping
# of LaTeX specials to produce valid TikZ. The trailing ``&`` replacement works
# around https://github.com/matplotlib/matplotlib/issues/15493.
_NO_ESCAPE = r"(?<!\\)(?:\\\\)*"
_re_mathsep = re.compile(_NO_ESCAPE + r"\$")
_replace_escapetext = functools.partial(
    # When the next character is _, ^, $, or % (not preceded by an escape),
    # insert a backslash.
    re.compile(_NO_ESCAPE + "(?=[_^$%])").sub,
    "\\\\",
)
_replace_mathdefault = functools.partial(
    # Replace \mathdefault (when not preceded by an escape) by empty string.
    re.compile(_NO_ESCAPE + r"(\\mathdefault)").sub,
    "",
)


def texify(text):
    """LaTeX-escape ``text`` for inclusion in TikZ/PGFPlots output."""
    text = _replace_mathdefault(text)
    text = text.replace("\N{MINUS SIGN}", r"\ensuremath{-}")
    # split into normal-text and inline-math segments
    parts = _re_mathsep.split(text)
    for i, s in enumerate(parts):
        if not i % 2:
            # textmode replacements
            s = _replace_escapetext(s)
        else:
            # mathmode replacements
            s = r"\(\displaystyle %s\)" % s  # noqa: UP031  (vendored from matplotlib)
        parts[i] = s
    return "".join(parts).replace("&", "\\&")


# ---------------------------------------------------------------------------
# Axes
# ---------------------------------------------------------------------------
def is_subplot(ax):
    """True if ``ax`` is laid out as a subplot (i.e. has a subplotspec).

    In matplotlib >= 3.7 ``mpl.axes.Subplot`` is merely an alias for
    ``mpl.axes.Axes``, so the historical ``isinstance(ax, Subplot)`` check is
    true for every axes. Query the subplotspec instead.
    """
    get_spec = getattr(ax, "get_subplotspec", None)
    return get_spec is not None and get_spec() is not None


# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
def legend_loc(legend):
    return legend._loc


def legend_ncols(legend):
    """Number of legend columns (``_ncol`` was renamed ``_ncols`` in mpl 3.6)."""
    try:
        return legend._ncols
    except AttributeError:
        return legend._ncol


def legend_bbox_to_anchor(legend):
    """The raw user-set bbox_to_anchor (``None`` if unset)."""
    return legend._bbox_to_anchor


def legend_box(legend):
    """The legend's offset box, used to measure its extent."""
    return legend._legend_box


def legend_handles(legend):
    """The legend's handles (``legendHandles`` was renamed in mpl 3.7)."""
    try:
        return legend.legend_handles
    except AttributeError:
        return legend.legendHandles


# ---------------------------------------------------------------------------
# Line2D dashes
# ---------------------------------------------------------------------------
def line_dash_pattern(line):
    """Return the unscaled ``(offset, sequence)`` dash pattern of a Line2D."""
    try:
        return line._unscaled_dash_pattern  # mpl >= 3.6
    except AttributeError:
        return (line._us_dashOffset, line._us_dashSeq)  # mpl < 3.6


def default_dash_pattern(style):
    """matplotlib's default ``(offset, sequence)`` dash pattern for ``style``."""
    return mpl.lines._get_dash_pattern(style)


# ---------------------------------------------------------------------------
# Axis unit converter
# ---------------------------------------------------------------------------
def axis_converter(axis):
    """The unit converter attached to an ``Axis``.

    ``Axis.converter`` was deprecated in matplotlib 3.10 (removed in 3.12) in
    favor of ``get_converter()``.
    """
    try:
        return axis.get_converter()
    except AttributeError:
        return axis.converter


# ---------------------------------------------------------------------------
# Colormaps
# ---------------------------------------------------------------------------
def cmap_segmentdata(cmap):
    return cmap._segmentdata


# ---------------------------------------------------------------------------
# Patches
# ---------------------------------------------------------------------------
def fancyarrow_posA_posB(patch):
    return patch._posA_posB


def patch_path_original(patch):
    return patch._path_original


def hatch_color(obj):
    """Resolved RGBA color of an artist's hatch.

    Recent matplotlib exposes a public ``get_hatchcolor()``. On older versions
    the color lives in the private ``_hatch_color``, which may hold the sentinel
    string ``"edge"`` (the default ``hatch.color`` rcParam): it means "use the
    edge color", but when the edge is fully transparent matplotlib falls back to
    ``rcParams["patch.edgecolor"]``. Mirror that resolution so the emitted hatch
    matches what matplotlib actually renders.
    """
    try:
        return obj.get_hatchcolor()
    except AttributeError:
        pass
    hc = obj._hatch_color
    if isinstance(hc, str):  # "edge" sentinel
        from matplotlib import colors

        if obj.get_edgecolor()[3] == 0:  # fully transparent edge
            return colors.to_rgba(mpl.rcParams["patch.edgecolor"])
        return obj.get_edgecolor()
    return hc
