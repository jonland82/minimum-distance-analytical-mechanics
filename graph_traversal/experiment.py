"""Deterministic structural measurements, not wall-clock speedup claims.

Run: python -m graph_traversal.experiment
"""
import csv
import json
from pathlib import Path
from platform import python_version

import numpy as np

from .traversal import radius_graph, separated_points, triangles

FOLDER = Path(__file__).resolve().parent


def run():
    rows = []
    cases = [("size", side, 1.7) for side in (8, 12, 20, 32, 48)]
    cases += [("range", 28, radius) for radius in (1.01, 1.3, 1.7, 2.1, 2.8, 3.6, 5.0)]
    for family, side, radius in cases:
        points = separated_points(side)
        graph = radius_graph(points, 1, radius)
        n = len(points)
        row = dict(family=family, side=side, n=n, k=1, radius=radius,
                   rho=radius, edges=graph.edges, max_degree=graph.max_degree,
                   triangles=sum(1 for _ in triangles(graph.adjacency)),
                   candidate_checks=graph.candidate_checks,
                   all_pairs=n*(n-1)//2, construction=graph.method)
        rows.append(row)
        print(f"{family:5s} n={n:4d} rho={radius:4.2f} "
              f"edges={graph.edges:5d} triangles={row['triangles']:6d} "
              f"checks={graph.candidate_checks:6d}/{row['all_pairs']}")
    with (FOLDER / "measurements.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (FOLDER / "environment.json").write_text(json.dumps({
        "python": python_version(), "numpy": np.__version__, "seed": 2026,
        "measurement": "counts, not timings", "k": 1,
        "point_family": "1.2-spaced square lattice, independent coordinate jitter in [-0.07,0.07]",
        "guaranteed_separation": 1.06,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
