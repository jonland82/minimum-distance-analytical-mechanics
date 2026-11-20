"""Run from the repository root with python -m routing_note.experiment."""

from platform import python_version, system
import csv
from pathlib import Path
from time import perf_counter

import numpy as np

from triangle_companion.one_stop import OneStopIndex, route_geometry


def scan(shortest, length, k):
    masked = np.where(shortest >= k, length, np.inf)
    i = masked.argmin()
    return (int(i), float(length[i])) if np.isfinite(masked[i]) else None


def run(n, batch):
    rng = np.random.default_rng(42)
    endpoints = ((0., 0.), (1., 0.))
    stops = rng.uniform(-1, 2, size=(n, 2))
    cutoffs = rng.uniform(.01, 1.05, size=batch)
    geometry = route_geometry(*endpoints, stops)
    for trial in range(6):
        start = perf_counter()
        index = OneStopIndex(*endpoints, stops)
        build = perf_counter() - start
        times = {}
        answers = {}
        for method in (("index", "scan") if trial % 2 else ("scan", "index")):
            start = perf_counter()
            if method == "index":
                answers[method] = [index.query(k) for k in cutoffs]
            else:
                answers[method] = [scan(*geometry, k) for k in cutoffs]
            times[method] = perf_counter() - start
        assert answers["index"] == answers["scan"]
        if trial:
            yield n, batch, trial, 1000 * build, 1000 * times["index"], 1000 * times["scan"]


if __name__ == "__main__":
    print(system(), python_version(), "NumPy", np.__version__)
    with Path(__file__).with_name("timings.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("n", "batch", "trial", "build", "lookup", "scan"))
        for count, batch in [(1000, 1000), (10000, 1000)] + [
            (100000, q) for q in (1, 32, 128, 256, 512, 1000)
        ]:
            writer.writerows(run(count, batch))
