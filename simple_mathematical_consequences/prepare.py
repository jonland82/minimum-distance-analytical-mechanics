"""Reproduce the note's figure and table, and check its numerical claims."""

from pathlib import Path
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)
LENGTH = 3 * math.sqrt(37) + 0.5 * math.asinh(6)


def count(k):
    return 2 * math.floor(min(3 / k, 3 / math.sqrt(k)))


def chord_length(n):
    x = np.linspace(-3, 3, n + 1)
    return math.fsum(np.hypot(np.diff(x), np.diff(x * x)))


def check_uniform_count(k):
    # Independently enumerate every count allowed by the horizontal-span bound,
    # using actual vertex coordinates rather than the closed-form parity rule.
    allowed = []
    for n in range(1, math.floor(6 / k) + 1):
        x = np.linspace(-3, 3, n + 1)
        if np.min(np.diff(x)) >= k - 1e-12 and np.min(np.abs(np.diff(x*x))) >= k - 1e-12:
            allowed.append(n)
    assert max(allowed, default=0) == count(k), (k, allowed)


def main():
    for k in [0.01, 0.1, 0.2, 0.5, 1, 2, 3, 3.01, 4]:
        check_uniform_count(k)

    nodes, weights = np.polynomial.legendre.leggauss(256)
    integrated_length = 3 * np.dot(weights, np.sqrt(1 + 36 * nodes**2))
    assert abs(integrated_length - LENGTH) < 1e-11
    rows = []
    for k in [1, 0.1, 0.01]:
        n = count(k)
        h = 6 / n
        estimate = chord_length(n)
        midpoints = -3 + (np.arange(n) + 0.5) * h
        midpoint_sum = h * math.fsum(np.sqrt(1 + 4 * midpoints**2))
        assert abs(estimate - midpoint_sum) < 1e-12
        error = LENGTH - estimate
        assert 0 < error <= h*h

        # Check every distinct vertex, including the right-angle corners.
        x = np.linspace(-3, 3, n + 1)
        points = np.vstack((np.column_stack((x, x*x)),
                            np.column_stack((x[1:], x[:-1]**2))))
        points = np.unique(points, axis=0)
        distances = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=2)
        np.fill_diagonal(distances, np.inf)
        assert distances.min() >= k - 1e-12

        rows.append(f"{k:g} & {n} & {estimate:.9f} & {error:.9f} \\\\")
        print(f"k={k:g}, N={n}, L_N={estimate:.12f}, E={error:.12f}")
    table = [r"\begin{tabular}{rrrr}", r"\toprule",
             r"Cutoff $k$ & Triangles $N(k)$ & Chord estimate $L_N$ & Error $E(k)$\\",
             r"\midrule", *rows, r"\bottomrule", r"\end{tabular}"]
    (ROOT / "results_table.tex").write_text("\n".join(table) + "\n", encoding="utf-8")

    # Confirm the leading error coefficient by an independent fine-grid sum.
    h = 6 / 1200
    coefficient = (LENGTH - chord_length(1200)) / h**2
    assert abs(coefficient - 1 / math.sqrt(37)) < 2e-7

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "pdf.fonttype": 42})
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.1),
                             gridspec_kw={"width_ratios": [1, 1.65]},
                             layout="constrained")
    for ax, n, extent, title in [
        (axes[0], 6, 3, "Six triangles"),
        (axes[1], 18, 1, "Near the vertex: eighteen-triangle grid")
    ]:
        curve_x = np.linspace(-extent, extent, 501)
        ax.plot(curve_x, curve_x**2, color="#2266aa", lw=2, label="Parabola")
        x = np.linspace(-3, 3, n + 1)
        for left, right in zip(x[:-1], x[1:]):
            if left < -extent - 1e-9 or right > extent + 1e-9:
                continue
            ax.plot([left, right], [left**2, right**2], color="#b45c22", lw=1.5)
            ax.plot([left, right, right], [left**2, left**2, right**2],
                    color="0.4", ls=":", lw=1)
        mask = np.abs(x) <= extent + 1e-9
        ax.scatter(x[mask], x[mask]**2, s=12, color="#b45c22", zorder=4)
        ax.set(xlabel="$x$", ylabel="$y$", title=title,
               xlim=(-extent - .15, extent + .15),
               ylim=(-.15, extent**2 + .2))
        ax.set_aspect("equal", adjustable="box")
        ax.grid(alpha=.15)
    axes[0].set_xticks([-3, 0, 3])
    axes[1].set_xticks([-1, 0, 1])
    axes[1].annotate("$h$", (-1/6, 0), xytext=(0, -13),
                     textcoords="offset points", ha="center")
    axes[1].annotate("$h^2$", (1/3, 1/18), xytext=(9, 0),
                     textcoords="offset points", va="center")
    fig.savefig(FIGURES / "parabola_triangles.pdf")
    fig.savefig(FIGURES / "parabola_triangles.png", dpi=200)
    plt.close(fig)
    print("Verified counts, vertex separation, quadrature, error bounds, and leading coefficient.")


def angle_figure():
    """Check the angular certificate on nonquadratic curves and draw it."""
    nodes, weights = np.polynomial.legendre.leggauss(256)
    h, bound = 3.0, 2.0
    def primitive(z):
        return 0.5 * (z * np.sqrt(1 + z*z) + np.arcsinh(z))
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.1), layout="constrained",
                             gridspec_kw={"width_ratios": [1, 1.3]})
    for row, epsilon in enumerate([0.02, 0.005, 0.0]):
        slope = 3 - 27*epsilon
        deficit = bound*h - 2*slope
        estimate = 2*(primitive(slope+3)-primitive(slope-3))/bound
        chord = 6*math.sqrt(1+slope*slope)
        true = 3*np.dot(weights, np.sqrt(1+(6*nodes-108*epsilon*nodes**3)**2))
        radius = 2*h*deficit
        low = max(chord, estimate-radius)
        high = min(chord+9, estimate+radius)
        assert low-1e-10 <= true <= high+1e-10
        if epsilon == 0:
            assert abs(estimate-LENGTH) < 1e-11
        axes[1].plot([chord, chord+9], [row+.1]*2, color="0.7", lw=5,
                     label="Chord bound" if row == 0 else None)
        axes[1].plot([low, high], [row-.1]*2, color="#2266aa", lw=5,
                     label="Combined bound" if row == 0 else None)
        axes[1].scatter([true], [row-.1], color="black", marker="o", zorder=5,
                        label="True length" if row == 0 else None)
        axes[1].scatter([estimate], [row-.1], color="#b45c22", marker="x", zorder=6,
                        label="Estimate" if row == 0 else None)
        print(f"epsilon={epsilon:g}, estimate={estimate:.9f}, true={true:.9f}, interval=[{low:.9f},{high:.9f}]")
    x = np.linspace(-3, 3, 501)
    axes[0].plot(x, 2*x-0.08*x**3, color="black", label="True slope")
    for left, right, slope in [(-3, 0, -2.46), (0, 3, 2.46)]:
        cell = np.linspace(left, right, 101)
        axes[0].plot(cell, slope+2*(cell-(left+right)/2), color="#2266aa")
        axes[0].plot([left, right], [slope, slope], color="#b45c22", ls=":")
    axes[0].plot([], [], color="#2266aa", label="Reconstructed slope")
    axes[0].plot([], [], color="#b45c22", ls=":", label="Chord slope")
    axes[0].set(xlabel="$x$", ylabel="Slope", title=r"$\varepsilon=0.02$")
    axes[0].legend(fontsize=8)
    axes[1].set(yticks=[0, 1, 2], yticklabels=["0.02", "0.005", "0"],
                ylabel=r"$\varepsilon$", xlabel="Arc length", ylim=(-.4, 2.5))
    axes[1].legend(fontsize=8, loc="upper right")
    for ax in axes:
        ax.grid(alpha=.15)
    fig.savefig(FIGURES / "angle_certificate.pdf")
    fig.savefig(FIGURES / "angle_certificate.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()
    angle_figure()
