"""Render vector figures from the worked example and recorded trial times."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

folder = Path(__file__).resolve().parent
blue, orange = "#245882", "#a84421"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, (ax, cost) = plt.subplots(1, 2, figsize=(7, 2.1), layout="constrained")
ax.plot([0, 2, 4], [0, 1, 0], "o-", color=orange)
ax.plot([0, 1, 4], [0, 0, 0], "o-", color=blue)
for x, y, label in [(0, 0, "A"), (1, 0, "V₁"), (2, 1, "V₂"), (4, 0, "B")]:
    ax.annotate(label, (x,y), xytext=(0, 7), textcoords="offset points", ha="center")
ax.set(xlim=(-.35, 4.35), ylim=(-.3, 1.6), aspect="equal", xlabel="Horizontal position", ylabel="Height")
r = np.sqrt(5)
for lo, hi, value, color in [(0, 1, 4, blue), (1, r, 2*r, orange)]:
    cost.plot([lo, hi], [value, value], color=color)
    cost.plot(lo, value, "o", markerfacecolor="white", color=color)
    cost.plot(hi, value, "o", color=color)
cost.axvspan(r, 3, color=".92")
cost.text(2.62, 4.22, "No route", ha="center")
cost.set(xlabel="Cutoff k", ylabel="Optimal length", xlim=(-.08,3), ylim=(3.88,4.61))
fig.savefig(folder / "route_geometry.pdf")
plt.close(fig)

data = np.genfromtxt(folder / "timings.csv", delimiter=",", names=True)
fig, axes = plt.subplots(1, 2, figsize=(7, 2.65), layout="constrained")
for ax, subset, key, xlabel in [
    (axes[0], data[data["batch"] == 1000], "n", "Candidate stops (1,000 queries)"),
    (axes[1], data[data["n"] == 100000], "batch", "Queries (100,000 stops)"),
]:
    xs = np.unique(subset[key])
    for values, label, color in [(subset["scan"], "Cached scan", orange),
                                 (subset["build"] + subset["lookup"], "Build + lookup", blue)]:
        low, mid, high = np.array([np.percentile(values[subset[key] == x], [0,50,100]) for x in xs]).T
        ax.fill_between(xs, low, high, color=color, alpha=.14)
        ax.loglog(xs, mid, "o-", color=color, label=label)
    ax.set(xlabel=xlabel, ylabel="Batch time (ms)")
    ax.legend(frameon=False, fontsize=8)
fig.savefig(folder / "runtime.pdf")
