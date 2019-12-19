"""Main functions in library."""
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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
    centers_, counts = compute_ntiles(data, dots=dots, hist_bins=hist_bins)
    centers = np.repeat(centers_, counts)
    counts = np.concatenate([np.arange(0.5, j + 0.5) for j in counts])

    axis = kwargs.pop("ax", None)
    if axis is None:
        axis = plt.gca()
    axis.figure.set_dpi(72.0)
    kwargs.setdefault("edgecolor", "black")
    kwargs.setdefault("linewidth", 1)

    circs = axis.scatter(centers, counts, s=1, **kwargs)
    axis.yaxis.set_major_locator(MaxNLocator(integer=True))

    if len(centers_) <= len(axis.get_xticks()):
        axis.set_xticks(centers_)
    bin_width = centers_[1] - centers_[0]
    axis.set_xlim(centers_[0] - bin_width, centers_[-1] + bin_width)

    axis.set_ylim(0, counts.max() + 1)
    diff = axis.transData.transform([(0, 1), (bin_width, 0), (0, 0)])
    x_scale = max(diff[0] - diff[-1])
    y_scale = max(diff[1] - diff[-1])
    if x_scale > y_scale:
        axis.set_ylim(0, (x_scale / y_scale) * (counts.max() + 1))
        diff = axis.transData.transform([(0, 1), (bin_width, 0), (0, 0)])

    size = max(diff[0] - diff[-1])
    circs.set_sizes([size ** 2 for _ in centers])
    return axis
