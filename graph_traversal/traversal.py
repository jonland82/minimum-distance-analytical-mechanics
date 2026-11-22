"""Local geometric graphs. Separation >= k is an input promise, not a filter.

Run from the repository root; only NumPy is required by this module.
The grid constructs the full radius graph. Other local graphs may delete edges.
"""
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import combinations
from math import ceil, floor, hypot, isfinite, sqrt

import numpy as np


@dataclass
class Graph:
    adjacency: list[dict[int, float]]
    candidate_checks: int
    method: str

    @property
    def edges(self):
        return sum(map(len, self.adjacency)) // 2

    @property
    def max_degree(self):
        return max(map(len, self.adjacency), default=0)


def radius_graph(points, k, radius):
    """Exact radius graph in real arithmetic; floating-point comparisons in code.

    Expected dictionary costs give O(n min(n, (1 + R/k)^2)) construction
    for k-separated planar input. The all-pairs fallback avoids empty-cell work
    when the search window is larger than the input. Weights are chord lengths.
    """
    points = np.asarray(points, dtype=float)
    if points.size == 0:
        points = points.reshape(0, 2)
    if points.ndim != 2 or points.shape[1] != 2 or not np.isfinite(points).all():
        raise ValueError("points must be a finite n-by-2 array")
    if not isfinite(k) or k <= 0 or not isfinite(radius) or radius < 0:
        raise ValueError("k must be positive and radius nonnegative, both finite")
    n = len(points)
    adjacency = [{} for _ in range(n)]
    checks = 0

    def consider(i, j):
        nonlocal checks
        checks += 1
        length = hypot(*(points[i] - points[j]))
        if length <= radius:
            adjacency[i][j] = length
            adjacency[j][i] = length

    if n <= 1:
        return Graph(adjacency, checks, "empty")
    width = k / sqrt(2)
    # Compare before enumerating cells; very large R/k uses the fallback.
    if radius / width >= sqrt(n):
        q = None
    else:
        q = ceil(radius / width)
    if q is None or (2 * q + 1) ** 2 >= n:
        for i in range(n):
            for j in range(i):
                consider(i, j)
        return Graph(adjacency, checks, "pairs")
    cells = {}
    for i, (x, y) in enumerate(points):
        cx, cy = floor(x / width), floor(y / width)
        for dx in range(-q, q + 1):
            for dy in range(-q, q + 1):
                for j in cells.get((cx + dx, cy + dy), ()):
                    consider(i, j)
        cells.setdefault((cx, cy), []).append(i)
    return Graph(adjacency, checks, "grid")


def dijkstra(adjacency, source):
    """Lazy binary-heap Dijkstra for finite, nonnegative edge weights."""
    n = len(adjacency)
    if not 0 <= source < n:
        raise ValueError("source is outside the graph")
    if any(not isfinite(w) or w < 0 for row in adjacency for w in row.values()):
        raise ValueError("edge weights must be finite and nonnegative")
    distance = [float("inf")] * n
    predecessor = [None] * n
    distance[source] = 0.0
    heap = [(0.0, source)]
    while heap:
        cost, u = heappop(heap)
        if cost != distance[u]:
            continue
        for v, weight in adjacency[u].items():
            candidate = cost + weight
            if candidate < distance[v]:
                distance[v], predecessor[v] = candidate, u
                heappush(heap, (candidate, v))
    return distance, predecessor


def triangles(adjacency):
    """List each graph triangle once, with u < v < w."""
    for u, neighbors in enumerate(adjacency):
        higher = sorted(v for v in neighbors if v > u)
        for v, w in combinations(higher, 2):
            if w in adjacency[v]:
                yield u, v, w


def separated_points(side, seed=2026):
    """A jittered lattice with a certified separation greater than k=1.

    Coordinate spacing 1.2 and jitter in [-.07,.07] imply every distinct
    pair differs by >= 1.06 along at least one coordinate.
    """
    rng = np.random.default_rng(seed)
    points = np.array([(x, y) for y in range(side) for x in range(side)], float)
    return 1.2 * points + rng.uniform(-.07, .07, points.shape)


def road_example(samples_per_segment=600):
    """The six-junction curved-road example; lengths use sampled arc length."""
    points = np.array([[60, 210], [245, 110], [255, 320],
                       [465, 125], [465, 315], [660, 210]], float)
    raw = [
        (0, 1, [[70,110,170,230,145,125], [120,25,245,40,245,110]]),
        (1, 3, [[300,20,315,185,365,85], [410,10,400,130,465,125]]),
        (0, 2, [[110,240,190,320,255,320]]),
        (2, 4, [[330,355,380,285,465,315]]),
        (4, 5, [[545,330,560,240,660,210]]),
        (3, 5, [[540,75,540,220,660,210]]),
        (2, 3, [[250,230,390,245,465,125]]),
        (3, 4, [[500,185,420,240,465,315]]),
    ]
    curves, adjacency = [], [{} for _ in points]
    for a, b, segments in raw:
        start = points[a]
        pieces = [start[None, :]]
        for values in segments:
            control = np.asarray(values, float).reshape(3, 2)
            t = np.linspace(0, 1, samples_per_segment + 1)[1:, None]
            u = 1 - t
            pieces.append(u**3 * start + 3*u*u*t*control[0]
                          + 3*u*t*t*control[1] + t**3*control[2])
            start = control[2]
        curve = np.vstack(pieces) / 100
        length = float(np.linalg.norm(np.diff(curve, axis=0), axis=1).sum())
        adjacency[a][b] = adjacency[b][a] = length
        curves.append((a, b, curve, length))
    return points / 100, curves, adjacency
