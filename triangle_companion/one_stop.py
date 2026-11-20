"""Exact one-stop Euclidean routes for repeated cutoff queries on a fixed corridor."""

from time import perf_counter

import numpy as np


def route_geometry(start, end, stops):
    """Return the triangle's shortest side and travel distance through each stop."""
    start, end, stops = (np.asarray(x, dtype=float) for x in (start, end, stops))
    if start.shape != (2,) or end.shape != (2,) or stops.ndim != 2 or stops.shape[1] != 2:
        raise ValueError("Expected two planar endpoints and an (n, 2) array of stops")
    if not all(np.isfinite(x).all() for x in (start, end, stops)):
        raise ValueError("Coordinates must be finite")
    first = np.hypot(*(stops - start).T)
    second = np.hypot(*(stops - end).T)
    shortest = np.minimum(np.minimum(first, second), np.hypot(*(end - start)))
    return shortest, first + second


class OneStopIndex:
    """Return the shortest feasible route, breaking distance ties by input index."""

    def __init__(self, start, end, stops):
        shortest, self.distance = route_geometry(start, end, stops)
        order = np.argsort(-shortest, kind="stable")
        self.keys = -shortest[order]
        self.best = np.empty(len(order), dtype=np.intp)
        winner = None
        for i, stop in enumerate(order):
            if winner is None or (self.distance[stop], stop) < (self.distance[winner], winner):
                winner = stop
            self.best[i] = winner

    def query(self, k):
        """Return (stop index, route length), or None if every route is excluded."""
        if not np.isfinite(k) or k <= 0:
            raise ValueError("Minimum separation must be positive and finite")
        count = self.keys.searchsorted(-k, side="right")
        if count == 0:
            return None
        stop = int(self.best[count - 1])
        return stop, float(self.distance[stop])


def benchmark():
    """Compare against a vectorized scan with all distances already cached."""
    rng = np.random.default_rng(42)
    start, end = (0., 0.), (1., 0.)
    stops = rng.uniform(-1, 2, size=(100_000, 2))
    cutoffs = rng.uniform(0.01, 1.05, size=1000)
    shortest, distance = route_geometry(start, end, stops)

    before = perf_counter()
    index = OneStopIndex(start, end, stops)
    built = perf_counter()
    answers = [index.query(k) for k in cutoffs]
    queried = perf_counter()
    for k, answer in zip(cutoffs, answers):
        masked = np.where(shortest >= k, distance, np.inf)
        i = int(masked.argmin())
        expected = (i, distance[i]) if np.isfinite(masked[i]) else None
        assert answer == expected
    checked = perf_counter()
    print(f"Index build {built-before:.4f}s, indexed queries {queried-built:.4f}s, "
          f"cached scans and verification {checked-queried:.4f}s")


if __name__ == "__main__":
    benchmark()
