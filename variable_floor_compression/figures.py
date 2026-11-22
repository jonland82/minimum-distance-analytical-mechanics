"""Render the worked example as vector PDF and high-resolution PNG."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "mathtext.fontset": "stix", "axes.spines.top": False,
                     "axes.spines.right": False, "axes.labelcolor": "#213337",
                     "text.color": "#213337", "xtick.color": "#56666A",
                     "ytick.color": "#56666A", "axes.edgecolor": "#CCD5D6"})
k = np.unique(np.r_[np.linspace(0, 12, 1201), 1, 2, 3, 6, 8, 10])
cost = np.maximum(k[:, None], [1, 3, 6, 10]).sum(axis=1)
summary = 2*np.maximum(k, 2) + 2*np.maximum(k, 8)
gap = cost-summary
assert np.max(gap) == 2
assert np.isclose(np.trapezoid(gap, k)/12, 5/12)
fig, (ax, err) = plt.subplots(1, 2, figsize=(6.7, 2.8),
                            gridspec_kw={"width_ratios": [1.2, 1]})
fig.subplots_adjust(left=.09, right=.98, bottom=.2, top=.82, wspace=.32)
for panel in (ax, err):
    panel.set_xlim(0, 12)
    panel.set_xticks([0, 2, 4, 6, 8, 10, 12])
    panel.set_xlabel(r"Edge-cost floor $k$")
    panel.grid(axis="y", color="#E6ECEC", lw=.7)
    panel.set_axisbelow(True)
ax.set_title("A  Chain cost", loc="left", fontweight="bold", pad=13)
ax.plot(k, cost, color="#213337", lw=2, label=r"Exact $C(k)$")
ax.plot(k, summary, color="#128675", lw=2, ls=(0, (4, 2)),
        label=r"Summary $\widehat C(k)$")
ax.fill_between(k, summary, cost, color="#128675", alpha=.14)
ax.set_ylabel("Total charge")
ax.set_ylim(17, 50)
ax.legend(frameon=False, loc="upper left", fontsize=8)
err.set_title("B  Compression error", loc="left", fontweight="bold", pad=13)
err.axhline(2, color="#B9763D", ls=(0, (3, 3)), lw=1)
err.plot(k, gap, color="#128675", lw=2)
err.fill_between(k, 0, gap, color="#128675", alpha=.14)
err.scatter([2, 8], [1, 2], color="#128675", s=25, zorder=4)
err.annotate(r"$A_1=1$", (2, 1), xytext=(0, 10),
             textcoords="offset points", ha="center")
err.annotate(r"$A_2=2$", (8, 2), xytext=(0, 10),
             textcoords="offset points", ha="center")
err.set_ylabel(r"$C(k)-\widehat C(k)$")
err.set_ylim(-.12, 2.65)
err.set_yticks([0, 1, 2])
fig.savefig(OUT / "floor_response.pdf", metadata={"CreationDate": None})
fig.savefig(OUT / "floor_response.png", dpi=300)
plt.close(fig)
print("Rendered figures/floor_response.pdf and .png")
