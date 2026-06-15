from types import SimpleNamespace

import numpy as np
import pytest
from matplotlib import pyplot as plt
from matplotlib.patches import ArrowStyle

from tikzplotlib import _mpl_compat


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def test_axis_accessors():
    _, ax = plt.subplots()
    ax.set_xscale("log", base=2)
    ax.tick_params(axis="x", direction="out")
    ax.grid(True, axis="x", which="major")

    assert _mpl_compat.axis_scale_base(ax.xaxis) == 2
    assert set(_mpl_compat.axis_tick_directions(ax.xaxis)) == {"out"}
    assert _mpl_compat.axis_grid_visible(ax.xaxis, "major")
    assert not _mpl_compat.axis_grid_visible(ax.xaxis, "minor")


def test_axis_accessors_fall_back_to_private_state():
    tick = SimpleNamespace(_tickdir="inout")
    axis = SimpleNamespace(
        get_major_ticks=lambda: [tick],
        get_minor_ticks=lambda: [],
        _minor_tick_kw={"gridOn": True},
    )

    assert _mpl_compat.axis_tick_directions(axis) == ["inout"]
    assert _mpl_compat.axis_grid_visible(axis, "minor")


def test_legend_bbox_anchor_point_uses_raw_coordinates():
    _, ax = plt.subplots()
    ax.plot([0, 1], label="line")
    legend = ax.legend(bbox_to_anchor=(0.2, 0.3))

    np.testing.assert_allclose(
        _mpl_compat.legend_bbox_anchor_point(legend),
        [0.2, 0.3],
    )


def test_line_drawstyle_prefers_public_api():
    _, ax = plt.subplots()
    (line,) = ax.plot([0, 1], drawstyle="steps-post")

    assert _mpl_compat.line_drawstyle(line) == "steps-post"
    assert _mpl_compat.line_drawstyle(SimpleNamespace(_drawstyle="steps-pre")) == (
        "steps-pre"
    )


def test_collection_offsets3d():
    ax = plt.figure().add_subplot(projection="3d")
    collection = ax.scatter([1, 2], [3, 4], [5, 6])

    offsets = _mpl_compat.collection_offsets3d(collection)

    np.testing.assert_array_equal(offsets[0], [1, 2])
    np.testing.assert_array_equal(offsets[1], [3, 4])
    np.testing.assert_array_equal(offsets[2], [5, 6])


def test_arrow_styles_prefers_public_api_and_falls_back():
    assert _mpl_compat.arrow_styles(ArrowStyle) == ArrowStyle.get_styles()

    private_styles = {"custom": object()}
    arrow_style_cls = SimpleNamespace(_style_list=private_styles)
    assert _mpl_compat.arrow_styles(arrow_style_cls) is private_styles
