"""Independent exact-arithmetic checks; run from any working directory."""
from fractions import Fraction as F
from itertools import combinations_with_replacement


def mean(block):
    return F(sum(block), len(block))


def error(block):
    mu = mean(block)
    return sum(abs(x - mu) for x in block) / 2


def partitions(values):
    for mask in range(1 << (len(values) - 1)):
        start, blocks = 0, []
        for i in range(len(values) - 1):
            if mask & (1 << i):
                blocks.append(values[start:i + 1])
                start = i + 1
        yield blocks + [values[start:]]


def greedy(values, tolerance):
    blocks, block = [], []
    for value in values:
        if block and error(block + [value]) > tolerance:
            blocks.append(block)
            block = []
        block.append(value)
    return blocks + [block]


def main():
    identities = optimality = routes = 0
    for size in range(1, 7):
        for values in combinations_with_replacement(range(5), size):
            choices = []
            for blocks in partitions(values):
                # Both functions are piecewise affine: these knots suffice
                # for an exact supremum and exact trapezoidal integration.
                knots = sorted({F(0), F(5), *map(F, values),
                                *(mean(b) for b in blocks)})
                gaps = [sum(max(x, k) for x in values)
                        - sum(len(b) * max(mean(b), k) for b in blocks)
                        for k in knots]
                bound = max(map(error, blocks))
                assert min(gaps) >= 0 and max(gaps) == bound
                integral = sum((y - x) * (a + b) / 2
                               for x, y, a, b in
                               zip(knots, knots[1:], gaps, gaps[1:]))
                variance = sum((x - mean(b)) ** 2 for b in blocks for x in b)
                assert integral / 5 == variance / 10
                choices.append((bound, len(blocks)))
                identities += 1
            for tolerance in {bound for bound, _ in choices}:
                optimum = min(count for bound, count in choices
                              if bound <= tolerance)
                assert len(greedy(values, tolerance)) == optimum
                optimality += 1

    # Three alternative s--t roads, each represented by one shortcut.
    # Enumerate all road-cost multisets of length three and all pairs
    # of competing direct costs. Check every knot and interval midpoint.
    for road in combinations_with_replacement(range(5), 3):
        for a in range(5):
            for b in range(5):
                roads = [road, (a,), (b,)]
                groups = [greedy(r, F(1)) for r in roads]
                bounds = [max(map(error, g)) for g in groups]
                knots = sorted({F(0), F(6), *map(F, road), F(a), F(b),
                                *(mean(g) for gs in groups for g in gs)})
                samples = knots + [(x+y)/2 for x,y in zip(knots, knots[1:])]
                for k in samples:
                    exact = [sum(max(x, k) for x in r) for r in roads]
                    approx = [sum(len(g)*max(mean(g), k) for g in gs)
                              for gs in groups]
                    chosen = min(range(3), key=approx.__getitem__)
                    assert 0 <= exact[chosen]-min(exact) <= bounds[chosen]
                    routes += 1
    print(f"PASS: {identities} exact uniform/expected-error checks; "
          f"{optimality} exhaustive greedy-optimality checks; "
          f"{routes} route-certificate checks.")


if __name__ == '__main__':
    main()
