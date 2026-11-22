"""Publication figures from fixed geometry and saved structural counts.

Run: python -m graph_traversal.figures
Outputs vector PDF and SVG, plus PNG previews, in graph_traversal/figures/.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle
import numpy as np

from .traversal import dijkstra, road_example

FOLDER = Path(__file__).resolve().parent
OUT = FOLDER / "figures"
INK, MUTED, GRID, GREEN, ORANGE = "#213337", "#6e8083", "#e3e9e7", "#128675", "#bf7843"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "text.color": INK,
    "axes.labelcolor": INK, "axes.edgecolor": GRID, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.titleweight": "medium", "axes.titlelocation": "left",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.spines.bottom": False,
    "axes.axisbelow": True, "grid.color": GRID, "grid.linewidth": .65,
    "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.facecolor": "white",
    "svg.fonttype": "none", "svg.hashsalt": "minimum-separation-traversal",
})


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    for suffix in ("pdf", "svg", "png"):
        target = OUT / f"{name}.{suffix}"
        metadata = {"CreationDate": None, "ModDate": None} if suffix == "pdf" else {"Date": None} if suffix == "svg" else None
        fig.savefig(target, dpi=200, bbox_inches="tight", pad_inches=.12, metadata=metadata)
        if suffix == "svg":
            target.write_text("\n".join(line.rstrip() for line in target.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


def roads():
    points, curves, adjacency = road_example()
    distance, previous = dijkstra(adjacency, 0)
    route = [5]
    while route[0] != 0:
        route.insert(0, previous[route[0]])
    selected = {tuple(sorted(pair)) for pair in zip(route, route[1:])}
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.35), layout="constrained")
    offsets = [(-.14,-.10), (0,-.19), (0,.19), (0,.22), (.05,.18), (.10,-.16), (-.08,-.15), (.24,0)]
    for ax, straight in zip(axes, (False, True)):
        ax.set_title("02   Graph abstraction" if straight else "01   Winding road geometry", fontsize=10, pad=8)
        for index, (a,b,curve,length) in enumerate(curves):
            xy = points[[a,b]] if straight else curve
            active = tuple(sorted((a,b))) in selected
            if active:
                ax.plot(*xy.T, color=GREEN, linewidth=8, alpha=.09, solid_capstyle="round", zorder=1)
            ax.plot(*xy.T, color=GREEN if active else MUTED,
                    linewidth=2.4 if active else 1.0, alpha=1 if active else .65,
                    solid_capstyle="round", zorder=2)
            position = (points[a]+points[b])/2 if straight else curve[len(curve)//2]
            offset = np.array(offsets[index])
            ax.text(*(position+offset), f"{length:.2f}", fontsize=8, ha="center", va="center",
                    bbox=dict(facecolor="white", edgecolor="none", pad=.5), zorder=3)
        for i, p in enumerate(points):
            terminal = i in (0,5)
            ax.scatter(*p, s=180 if terminal else 145, facecolor=INK if terminal else "white",
                       edgecolor=INK if terminal else "#cbd8d4", linewidth=.9, zorder=5)
            ax.text(*p, chr(65+i), color="white" if terminal else INK, ha="center", va="center", fontsize=8, zorder=6)
            if terminal:
                ax.text(p[0], p[1]+.29, "Start" if i==0 else "Finish", ha="center", color=MUTED, fontsize=7.5)
        ax.set(xlim=(.1,7.1), ylim=(3.75,.12), aspect="equal")
        ax.axis("off")
    fig.supxlabel(f"Same edge costs, same shortest route: A → C → E → F  ·  {distance[5]:.2f} km", fontsize=9, color=INK)
    save(fig, "road_network")


def packing():
    k, radius = 1., 2.
    lattice=[]
    for j in range(-4,5):
        for i in range(-4,5):
            p=np.array([i+.5*(j%2), j*np.sqrt(3)/2])
            if np.linalg.norm(p) <= radius+1e-12:
                lattice.append(p)
    points=np.array(lattice)
    fig, ax=plt.subplots(figsize=(5.6,4.3), layout="constrained")
    ax.add_patch(Circle((0,0),radius+k/2,facecolor=GREEN,alpha=.035,edgecolor="none"))
    ax.add_patch(Circle((0,0),radius+k/2,fill=False,edgecolor=GREEN,lw=1.1))
    ax.add_patch(Circle((0,0),radius,fill=False,edgecolor=MUTED,lw=.8,linestyle=(0,(4,4))))
    for p in points:
        ax.add_patch(Circle(p,k/2,facecolor=GREEN,edgecolor=GREEN,alpha=.11,lw=.8))
    ax.scatter(*points.T,s=18,color=GREEN,zorder=3)
    ax.scatter(0,0,s=36,color=INK,zorder=4)
    ax.annotate("Connection radius R",xy=(1.36,1.46),xytext=(2.65,1.6),
                fontsize=9,arrowprops=dict(arrowstyle="-",color=MUTED,lw=.8),ha="left")
    ax.annotate("Containing radius R + k/2",xy=(1.85,-1.68),xytext=(2.65,-1.6),
                fontsize=9,arrowprops=dict(arrowstyle="-",color=MUTED,lw=.8),ha="left")
    ax.annotate("Disjoint disks of radius k/2",xy=(-.95,.4),xytext=(-3.2,2.95),
                fontsize=9,arrowprops=dict(arrowstyle="-",color=MUTED,lw=.8))
    ax.set(xlim=(-3.3,5.5),ylim=(-2.8,3.3),aspect="equal")
    ax.axis("off")
    save(fig,"packing_bound")


def measurements():
    data=np.genfromtxt(FOLDER/"measurements.csv",delimiter=",",names=True,dtype=None,encoding="utf-8")
    fixed=data[data["family"]=="size"]
    varied=data[data["family"]=="range"]
    fig,axes=plt.subplots(1,2,figsize=(7.1,2.9),layout="constrained")
    ax=axes[0]
    ax.loglog(fixed["n"],fixed["all_pairs"],color=MUTED,linestyle="--",label="All vertex pairs")
    ax.loglog(fixed["n"],fixed["candidate_checks"],"o-",color=GREEN,markersize=4,label="Grid distance checks")
    ax.set(xlabel="Vertices n",ylabel="Pairwise distance evaluations",title="Local search avoids distant pairs")
    ax.grid(True,which="major")
    ax.legend(frameon=False,fontsize=7.5,loc="upper left")
    ax=axes[1]
    ax.plot(fixed["n"],fixed["edges"]/fixed["n"],"o-",color=GREEN,markersize=4,label="Edges / vertex")
    ax.plot(fixed["n"],fixed["triangles"]/fixed["n"],"s-",color=ORANGE,markersize=4,label="Triangles / vertex")
    ax.set(xlabel="Vertices n",ylabel="Count divided by n",ylim=(0,3.5),title="Fixed R/k = 1.7")
    ax.grid(axis="y")
    ax.legend(frameon=False,fontsize=7.5,loc="lower right")
    save(fig,"network_growth")
    fig,axes=plt.subplots(1,2,figsize=(7.1,2.9),layout="constrained")
    rho=np.linspace(1,5,200)
    ax=axes[0]
    ax.plot(rho,(1+2*rho)**2-1,color=MUTED,linestyle="--",label="Area upper bound")
    ax.plot(varied["rho"],varied["max_degree"],"o-",color=GREEN,markersize=4,label="Observed maximum")
    ax.set(xlabel="Connection-to-separation ratio R/k",ylabel="Maximum degree",title="Larger range admits more neighbors")
    ax.grid(axis="y")
    ax.legend(frameon=False,fontsize=7.5,loc="upper left")
    ax=axes[1]
    ax.plot(varied["rho"],varied["triangles"]/varied["n"],"s-",color=ORANGE,markersize=4)
    ax.set(xlabel="Connection-to-separation ratio R/k",ylabel="Triangles / vertex",title="Fixed n = 784; varying R/k")
    ax.grid(axis="y")
    save(fig,"range_sensitivity")


if __name__ == "__main__":
    roads()
    packing()
    measurements()
    print("Wrote four figures in PDF, SVG, and PNG formats.")
