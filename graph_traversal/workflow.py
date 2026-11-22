"""Render the paper's argument as a standalone companion diagram.

Run from the repository root: python -m graph_traversal.workflow
"""
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from .figures import GREEN, GRID, INK, MUTED, save


def run():
    fig, ax = plt.subplots(figsize=(12, 12.8))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set(xlim=(0, 12), ylim=(0, 12.8))
    ax.axis("off")

    ax.text(.55, 12.15, "From minimum distance to graph traversal",
            fontsize=23, weight="medium", va="center")
    ax.text(.55, 11.68, "How the paper's assumptions become bounds and algorithms",
            fontsize=12.5, color=MUTED)
    ax.text(.55, 11.26, "Solid arrows: dependencies     Dashed links: supporting context and evidence",
            fontsize=10, color=MUTED)

    left, width, height = .55, 7.05, 1.42
    centers = [10.18, 8.36, 6.54, 4.72, 2.90]
    steps = [
        ("01", "Set the rules", "Model",
         "Vertices stay at least k apart, and edges join endpoints at most R apart.",
         r"Fixed dimension $d$; connection-to-separation ratio $\rho = R/k$"),
        ("02", "Count nearby vertices", "Theorem 2 · Packing",
         "Each vertex needs space around it, so only a bounded number fit in a neighborhood.",
         r"Local occupancy: $|P \cap B(x,r)| \leq (1 + 2r/k)^d$"),
        ("03", "Bound the graph's size", "Corollary 3",
         "Apply the neighborhood bound at radius R to limit neighbors, edges, and graph triangles.",
         r"$\Delta \leq (1+2R/k)^d-1$; fixed $d,\,R/k$ gives $m,T=O(n)$"),
        ("04", "Build the local graph", "Theorem 4 · Construction",
         "A spatial grid checks nearby candidates to construct the full radius graph efficiently.",
         r"Fixed $d,\,R/k$: expected $O(n)$ construction with spatial hashing"),
        ("05", "Traverse and find routes", "Standard algorithms",
         "The sparse graph supports efficient traversal, triangle listing, and weighted shortest paths.",
         r"BFS: $O(n)$   ·   Dijkstra: $O(n\log n)$   ·   triangle listing: expected $O(n)$"),
    ]

    def rounded(x, y, w, h, face, edge="none"):
        patch = FancyBboxPatch((x, y), w, h,
                              boxstyle="round,pad=0.015,rounding_size=0.10",
                              facecolor=face, edgecolor=edge, linewidth=.8)
        ax.add_patch(patch)

    for center, (number, title, label, sentence, formula) in zip(centers, steps):
        bottom = center-height/2
        rounded(left, bottom, width, height, "#f1f7f5")
        ax.text(left+.21, bottom+height-.29, number, fontsize=10,
                weight="medium", color=GREEN, va="center")
        ax.text(left+.65, bottom+height-.29, title, fontsize=14,
                weight="medium", va="center")
        ax.text(left+width-.20, bottom+height-.29, label, fontsize=8.3,
                color=MUTED, ha="right", va="center")
        ax.text(left+.22, bottom+height-.64,
                textwrap.fill(sentence, width=78), fontsize=11.1,
                va="top", linespacing=1.45)
        ax.text(left+.22, bottom+.18, formula, fontsize=9.9,
                va="center", color=INK)

    spine = left+width/2
    for upper, lower in zip(centers, centers[1:]):
        ax.add_patch(FancyArrowPatch((spine, upper-height/2-.06),
                                    (spine, lower+height/2+.06),
                                    arrowstyle="-|>", mutation_scale=14,
                                    linewidth=1.4, color=GREEN))

    side_left, side_width = 8.12, 3.28
    def support(center, title, reference, sentence, h=1.66):
        bottom = center-h/2
        rounded(side_left, bottom, side_width, h, "#f7f8f8", GRID)
        ax.text(side_left+.19, bottom+h-.25, reference, fontsize=9,
                color=MUTED, va="center")
        ax.text(side_left+.19, bottom+h-.56, title, fontsize=12,
                weight="medium", va="center")
        ax.text(side_left+.19, bottom+h-.86,
                textwrap.fill(sentence, width=35), fontsize=10.4,
                va="top", linespacing=1.5)
        ax.plot([left+width+.07, side_left-.07], [center, center],
                color=MUTED, linewidth=1, dashes=(3, 3))

    support(centers[0], "Why use both rules?", "Proposition 1 · Context",
            "Separated vertices can still all connect, so a range limit controls their neighbors.", h=1.83)
    support(centers[2], "Measure and verify", "Experiments · Implementation checks",
            "Structural counts illustrate the bounds; independent reference methods check the code.", h=1.83)
    support(centers[4], "Preserve road costs", "Winding-road example",
            "Keeping actual road lengths as weights preserves optimal routes when the drawing is straightened.", h=1.98)

    rounded(.55, .52, 10.85, .93, INK)
    ax.text(.80, 1.12, "What the paper establishes", fontsize=11.3,
            weight="medium", color="white", va="center")
    ax.text(.80, .80,
            "Explicit bounds and reproducible algorithms connecting separation + locality to computational work.",
            fontsize=10.5, color="#e2eeea", va="center")
    ax.text(.55, .20, "Companion to Minimum Separation and Locality in Geometric Graph Traversal",
            fontsize=8.5, color=MUTED)
    save(fig, "paper_workflow")
    print("Wrote figures/paper_workflow.png, .pdf, and .svg")


if __name__ == "__main__":
    run()
