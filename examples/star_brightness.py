import pathlib

import matplotlib.pyplot as plt
import numpy as np

from quantile_dotplot import ntile_dotplot

if __name__ == "__main__":
    here = pathlib.Path(__file__).resolve().parent

    for width, dots, bins in zip((7, 14, 9), (20, 50, 100), ("auto", 20, 20)):
        fig, ax = plt.subplots(figsize=(width, 4))
        data = np.load(here / "magnitudes.npz")["arr"]
        circs = ntile_dotplot(data, dots=dots, hist_bins=bins, fc="k", ax=ax)

        ax.set_title(f"{dots} dots, {bins} hist_bins")
        ax.set_xlabel("Red band magnitude (inverted, logarithmic)")
        for spine in ("left", "right", "top"):
            ax.spines[spine].set_visible(False)
        ax.yaxis.set_visible(False)

        fig.savefig(here / "figures" / f"star_brightness{width}.png")
