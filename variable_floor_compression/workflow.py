"""Render the companion argument diagram; run from any working directory."""
from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

INK, GREEN, MUTED = "#213337", "#128675", "#637579"


def run():
    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK,
                         "mathtext.fontset": "cm", "svg.hashsalt": "floor-workflow",
                         "text.latex.preamble": r"\usepackage{amssymb}"})
    fig, ax = plt.subplots(figsize=(12, 15.5))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set(xlim=(0, 12), ylim=(0, 15.5))
    ax.axis("off")
    ax.text(.55, 14.85, "Store less about each road. Bound the error.",
            fontsize=26, weight="medium")
    ax.text(.55, 14.37, "Compact Road Shortcuts with Guaranteed Error",
            fontsize=15, color=MUTED)
    ax.text(.55, 13.91, "Read down: problem → summary → error bound → grouping algorithm → route guarantee",
            fontsize=12, color=MUTED)

    def box(x, y, w, h, color, edge="none"):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                     boxstyle="round,pad=0.015,rounding_size=.10",
                     facecolor=color, edgecolor=edge, linewidth=.8))

    centers = [12.60, 10.40, 8.20, 6.00, 3.80]
    height, left, width = 1.95, .55, 7.05
    steps = [
        ("01", "Start with a road made of many edges", "THE PROBLEM / SECTION 1",
         "Each query sets a minimum edge charge k. Raise smaller costs to k, then add them to get the road's cost.",
         r"$\displaystyle C(k)=\sum_{i=1}^{h}\max(w_i,k)$"),
        ("02", "Replace many costs with a few group means", "THE SUMMARY / SECTION 1",
         "Sort the edge costs and group adjacent entries. Store each group's count and mean to estimate the road's cost.",
         r"$\displaystyle \widehat C(k)=\sum_{j=1}^{r}h_j\max(\mu_j,k)$"),
        ("03", "Prove how far the estimate can fall short", "THEOREM 1 / SECTION 2",
         r"The estimate is always too low or exact. Its largest shortfall over every k equals the largest group error $A_j$.",
         r"$\displaystyle \sup_{k\geq0}(C-\widehat C)=\max_j A_j,\quad A_j=\frac12\sum_{i\in G_j}|w_i-\mu_j|$"),
        ("04", "Choose an error limit, then form groups", "THEOREM 2 / SECTION 4",
         "Keep adding costs until the group would exceed the limit. This uses the fewest groups of the form in step 2.",
         r"$\displaystyle A_j\leq\varepsilon;\qquad\mathrm{build}:\ \mathcal O(h\log(h+1))$"),
        ("05", "Use the summaries to choose a route", "COROLLARY 3 / SECTION 5",
         "Add the error limits of the roads on the chosen route. This bounds how much more it costs than the true best route.",
         r"$\displaystyle 0\leq C(\widehat P,k)-d(k)\leq\sum_{e\in\widehat P}\varepsilon_e$"),
    ]
    for center, (number, title, label, prose, formula) in zip(centers, steps):
        y = center-height/2
        box(left, y, width, height, "#f1f7f5")
        ax.text(left+.22, y+1.66, number, fontsize=12, color=GREEN, weight="bold")
        ax.text(left+.65, y+1.66, title, fontsize=15, weight="medium")
        ax.text(left+.22, y+1.34, label, fontsize=10, color=MUTED)
        ax.text(left+.22, y+1.08, textwrap.fill(prose, 67), fontsize=12.5,
                va="top", linespacing=1.4)
        ax.text(left+.22, y+.30, formula, fontsize=14, usetex=True,
                fontfamily="serif", va="center")
    for upper, lower in zip(centers, centers[1:]):
        ax.add_patch(FancyArrowPatch((4.075, upper-height/2-.05),
                     (4.075, lower+height/2+.05), arrowstyle="-|>",
                     mutation_scale=14, color=GREEN, linewidth=1.4))

    def side(center, title, label, prose, formula=None):
        x, w = 8.10, 3.30
        h = 2.65 if formula else 2.15
        y = center-h/2
        box(x, y, w, h, "#f7f8f8", "#dae3e2")
        ax.text(x+.18, y+h-.30, label, fontsize=10, color=MUTED)
        ax.text(x+.18, y+h-.66, title, fontsize=14, weight="medium")
        ax.text(x+.18, y+h-.98, textwrap.fill(prose, 31), fontsize=12,
                va="top", linespacing=1.45)
        if formula:
            ax.text(x+.18, y+.25, formula, fontsize=13,
                    usetex=True, fontfamily="serif")
        ax.plot([7.68, 8.02], [center, center], color=MUTED,
                linewidth=1, dashes=(3, 3))

    side(centers[0], "Why a sum is not enough", "EXAMPLE / SECTION 1",
         "Two edges costing 1 each cost 6 at k = 3. Storing their sum, 2, and raising it to 3 loses half the charge.")
    side(centers[2], "Average error", "THEOREM 1 / SECTIONS 2–3",
         r"For k uniform on [0, U], average error uses $V_j$: squared deviations from each group's mean. Costs are at most U.",
         r"$\displaystyle \mathbb E[C-\widehat C]=\frac{1}{2U}\sum_j V_j$")
    side(centers[4], "Reuse for each new k", "QUERY COST / SECTION 5",
         "For each new k, search the stored means to estimate a road's cost. Here r is the number of stored groups.",
         r"$\displaystyle \mathcal O(\log(r+1))\ \mathrm{time};\ \mathcal O(r)\ \mathrm{space}$")

    box(.55, .57, 10.85, 1.65, INK)
    ax.text(.80, 1.88, "What we gain", fontsize=15,
            color="white", weight="medium")
    ax.text(.80, 1.53, "Fewest groups for an error limit; a bound on the route's extra cost.",
            fontsize=13.5, color="#e2eeea")
    ax.text(.80, 1.13,
            r"Per-shortcut lookup: $\mathcal O(\log(h+1))\to\mathcal O(\log(r+1))$.",
            fontsize=16, color="#e2eeea", usetex=True, fontfamily="serif")
    ax.text(.80, .76,
            r"Summary space: $\mathcal O(h)\to\mathcal O(r)$, with $r\leq h$.",
            fontsize=16, color="#e2eeea", usetex=True, fontfamily="serif")
    ax.text(.55, .20, "h: original edges   r: groups   k: cost floor   d(k): exact shortest distance",
            fontsize=12, color=MUTED)
    out = Path(__file__).resolve().parent / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "paper_workflow.pdf", metadata={"CreationDate": None})
    fig.savefig(out / "paper_workflow.png", dpi=200)
    fig.savefig(out / "paper_workflow.svg", metadata={"Date": None})
    plt.close(fig)
    print("Rendered figures/paper_workflow.png, .pdf, and .svg")


if __name__ == "__main__":
    run()
