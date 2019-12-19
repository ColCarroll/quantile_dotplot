import pathlib

import matplotlib.pyplot as plt
import numpy as np

from quantile_dotplot import ntile_dotplot
import matplotlib


if __name__ == "__main__":
    here = pathlib.Path(__file__).resolve().parent

    fig, ax = plt.subplots(figsize=(10, 7))
    data = np.random.lognormal(mean=np.log(11.4), sigma=0.2, size=1_000_000)

    ax = ntile_dotplot(data, dots=20, edgecolor="k", linewidth=2, ax=ax)

    ax.set_xlabel("Minutes to bus")
    for spine in ("left", "right", "top"):
        ax.spines[spine].set_visible(False)
    ax.yaxis.set_visible(False)
    fig.savefig(here / "figures" / "bus_times.png")
