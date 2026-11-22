"""Independent checks of construction, packing, triangles, and route costs.

Run: python -m graph_traversal.validate
"""
from itertools import combinations
from math import comb, hypot, sqrt

import numpy as np
from scipy.sparse.csgraph import shortest_path

from .traversal import dijkstra, radius_graph, road_example, separated_points, triangles


def brute_graph(points, radius):
    adjacency = [{} for _ in points]
    for i, j in combinations(range(len(points)), 2):
        length = hypot(*(points[i] - points[j]))
        if length <= radius:
            adjacency[i][j] = adjacency[j][i] = length
    return adjacency


def matrix(adjacency):
    n = len(adjacency)
    out = np.full((n, n), np.inf)
    np.fill_diagonal(out, 0)
    for i, row in enumerate(adjacency):
        for j, w in row.items():
            out[i, j] = w
    return out


def run():
    checks = 0
    # Exact-radius equality, negative cells, and non-integer R/cell width.
    boundary = np.array([[-2., 0.], [-1., 0.], [0., 0.], [0., 1.], [1., 1.]])
    for points in (boundary, separated_points(4), separated_points(11)):
        for radius in (0., 1., sqrt(2), 1.7, 2.8, 100.):
            graph = radius_graph(points, 1, radius)
            reference = brute_graph(points, radius)
            assert graph.adjacency == reference
            checks += 1
            delta = graph.max_degree
            assert delta + 1 <= (1 + 2*radius)**2 + 1e-10
            assert graph.edges <= len(points)*delta/2
            observed = set(triangles(graph.adjacency))
            expected = {(u,v,w) for u,v,w in combinations(range(len(points)),3)
                        if v in reference[u] and w in reference[u] and w in reference[v]}
            assert observed == expected
            assert len(observed) <= len(points)*delta*(delta-1)/6
            checks += 1
            oracle = shortest_path(matrix(reference), directed=False, method="FW")
            for source in (0, len(points)-1):
                actual, _ = dijkstra(graph.adjacency, source)
                np.testing.assert_allclose(actual, oracle[source])
                checks += 1
    assert radius_graph([], 1, 1).adjacency == []
    assert radius_graph([[0,0]], 1, 1).edges == 0
    checks += 2
    # An equilateral metric shows that uniform discreteness alone does not
    # even imply a local occupancy bound in an arbitrary metric space.
    n = 25
    complete = [{j: 1. for j in range(n) if j != i} for i in range(n)]
    assert sum(1 for _ in triangles(complete)) == comb(n,3)
    checks += 1
    # Winding geometry can change the winner, but straightening the drawing
    # with weights preserved cannot change any distance.
    points, curves, adjacency = road_example()
    distance, previous = dijkstra(adjacency, 0)
    route = [5]
    while route[0] != 0:
        route.insert(0, previous[route[0]])
    assert route == [0, 2, 4, 5]
    np.testing.assert_allclose(distance, shortest_path(matrix(adjacency), method="FW")[0])
    chords = [{j: hypot(*(points[i]-points[j])) for j in row}
              for i, row in enumerate(adjacency)]
    _, previous_chord = dijkstra(chords, 0)
    chord_route = [5]
    while chord_route[0] != 0:
        chord_route.insert(0, previous_chord[chord_route[0]])
    assert chord_route == [0, 1, 3, 5]
    assert all(length + 1e-12 >= hypot(*(points[a]-points[b]))
               for a,b,_,length in curves)
    _, _, refined = road_example(1200)
    np.testing.assert_allclose(matrix(adjacency), matrix(refined), rtol=1e-5)
    checks += 5
    print(f"PASS: {checks} grouped checks; brute-force adjacency and triangles; "
          "Floyd-Warshall distances; boundary cases; road-length refinement.")


if __name__ == "__main__":
    run()
