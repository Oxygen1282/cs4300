"""Task 7: matplotlib plots the data and saves it as an image."""
import matplotlib

matplotlib.use("Agg")   # draw without a screen (the container has none)

import matplotlib.pyplot as plt
import pytest

from conftest import SRC
import runpy


@pytest.fixture
def plotted(tmp_path, monkeypatch):
    """Run task7 inside a temporary folder so the saved image doesn't
    clutter the project, then hand back that folder and the plotted line."""
    plt.close("all")                      # start each test with no figures
    monkeypatch.chdir(tmp_path)
    variables = runpy.run_path(str(SRC / "task7.py"))
    line = plt.gca().get_lines()[0]
    yield tmp_path, variables, line
    plt.close("all")


def test_image_file_saved(plotted):
    """savefig with no extension saves a PNG, so task7_output.png must
    exist and not be empty."""
    folder, _, _ = plotted
    image = folder / "task7_output.png"
    assert image.exists()
    assert image.stat().st_size > 0


def test_file_is_really_a_png(plotted):
    """Every PNG starts with the same 8 'magic' bytes. Checking them
    proves matplotlib wrote a real image, not an empty or broken file."""
    folder, _, _ = plotted
    assert (folder / "task7_output.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_plotted_data_matches(plotted):
    """The line on the chart holds exactly the x and y lists from the script."""
    _, variables, line = plotted
    assert list(line.get_xdata()) == variables["x"]
    assert list(line.get_ydata()) == variables["y"]


def test_line_style(plotted):
    """The styling passed to plt.plot was applied."""
    _, _, line = plotted
    assert line.get_marker() == "o"
    assert line.get_linestyle() == "-"
    assert matplotlib.colors.to_hex(line.get_color()) == "#ff0000"   # red


def test_points_sorted_by_x(plotted):
    """The points are sorted left to right, and none were lost or changed:
    sorting the original pairs gives exactly the plotted pairs."""
    _, variables, line = plotted
    xs = list(line.get_xdata())
    assert xs == sorted(xs)
    original = sorted(zip(variables["x_raw"], variables["y_raw"]))
    assert list(zip(xs, line.get_ydata())) == original


def test_labels_and_legend(plotted):
    """The graph has a title, both axis labels and a legend."""
    ax = plt.gca()
    assert ax.get_title() != ""
    assert ax.get_xlabel() == "X value"
    assert ax.get_ylabel() == "Y value"
    assert ax.get_legend() is not None


def test_average_line(plotted):
    """The dashed line sits at the mean of the y values, (sum / count)."""
    _, variables, _ = plotted
    average_line = plt.gca().get_lines()[1]
    expected = sum(variables["y_raw"]) / len(variables["y_raw"])
    assert average_line.get_ydata()[0] == pytest.approx(expected)
    assert average_line.get_linestyle() == "--"


def test_peak_annotated(plotted):
    """The annotation points at the highest point, (17, 36)."""
    annotations = [t for t in plt.gca().texts if t.get_text().startswith("Peak")]
    assert len(annotations) == 1
    assert annotations[0].xy == (17, 36)