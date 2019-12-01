"""Main functions in library."""
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Ellipse
import numpy as np

__all__ = ["compute_ntiles", "ntile_dotplot"]


def compute_ntiles(data: np.ndarray, *, dots, hist_bins):
    """Compute an ntile partition for the data.

    Parameters:
    -----------
    data : iterable
        Empirical data from a distribution.
    dots : int
        Number of dots in the quantile dot plot.
    hist_bins : int or str
        If an integer, the number of histogram bins to put the dots in. If 'auto',
        will choose the number of bins so that the tallest bin is about as high as
        the number of bins.

    Returns:
    --------
    ndarray, ndarray:
        the centers of the quantiles (x-values)
        the number of dots in each of these bins

    """
    data = np.array(data)
    edge = (100 / dots) / 2
    grouped = np.percentile(
        data.ravel(), np.linspace(edge, 100 - edge, num=dots, endpoint=True)
    )
    if hist_bins == "auto":
        bins = 1
        counts, centers = np.histogram(grouped, bins=bins)
        while counts.max() + 2 > len(counts):
            bins += 1
            counts, centers = np.histogram(grouped, bins=bins)
    else:
        counts, centers = np.histogram(grouped, bins=hist_bins)
    bin_width = centers[1] - centers[0]
    centers = centers[:-1] + 0.5 * bin_width
    return centers, counts


def ntile_dotplot(data, dots=10, hist_bins="auto", **kwargs):
    """Make an ntile dotplot out of the data.

    Parameters:
    -----------
    data : iterable
        Empirical data from a distribution.
    dots : int
        Number of dots in the quantile dot plot.
    hist_bins : int or str
        If an integer, the number of histogram bins to put the dots in. If 'auto',
        will choose the number of bins so that the tallest bin is about as high as
        the number of bins.
    ax : matplotlib.Axes (Optional)
        Axis to plot on. If not provided, attempts to plot on current axes.
    kwargs :
        Passed to the PatchCollection artist.

    Returns:
    --------
    PatchCollection :
        The collection of artists added to the axes.

    """
    centers, counts = compute_ntiles(data, dots=dots, hist_bins=hist_bins)
    bin_width = centers[1] - centers[0]
    xlims = centers.min() - bin_width, centers.max() + bin_width
    y_ratio = (xlims[1] - xlims[0]) / (counts.max() - 1)
    ylims = (0.5, counts.max() + 1.0)
    centers = np.repeat(centers, counts)
    counts = np.concatenate([np.arange(1, j + 1) for j in counts])

    axis = kwargs.pop("ax", None)
    if axis is None:
        axis = plt.gca()
    patches = [
        Ellipse(center, width=min(bin_width, y_ratio), height=1)
        for center in zip(centers, counts)
    ]
    circs = PatchCollection(patches, **kwargs)
    circs = axis.add_collection(circs)
    axis.set_ylim(*ylims)
    axis.set_xlim(*xlims)
    return circs
