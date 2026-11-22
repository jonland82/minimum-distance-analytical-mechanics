# Compact Road Shortcuts with Guaranteed Error

[Read the five-page note](chain_compression.pdf) · [LaTeX source](chain_compression.tex)

For repeated queries with edge-cost floor `k`, summarize each road chain by consecutive groups of its sorted edge costs. Each group retains its size and mean. The note proves:

- The exact worst-case error across all floors equals the largest group's half-sum of absolute deviations from its mean.
- With a uniform floor on `[0, U]` covering all edge costs, expected chain error equals total within-group squared deviations divided by `2U`.
- Longest-admissible-group construction minimizes the number of groups for a prescribed uniform error within the consecutive mean-summary family.
- Summing shortcut error certificates along the selected route bounds its excess cost relative to exact routing under the same floor.

The scope is finite nonnegative costs and repeated floor queries. Graph contraction preserves terminals and parallel roads. Sorting is for cost summaries; expanding a route uses the retained original road order. Summary storage is separate from the storage needed to reconstruct roads. The expectation is for a fixed chain; a route selected using the realized floor requires accounting for selection.

The note builds on the repository's [edge-floor error derivation](../graph_traversal/edge_floor_error.pdf) and [changing-cutoff routing note](../routing_note/one_stop_routing.pdf). Related literature includes approximate shortcut functions and stop-loss transforms. Originality remains provisional: the note makes no priority claim or claim of a new general shortest-path algorithm.

## Reproduce

From the repository root:

```powershell
python variable_floor_compression/validate.py
python variable_floor_compression/figures.py
```

Validation uses only the Python standard library. It exhaustively checks sorted multisets with one to six costs from `{0,1,2,3,4}`, every consecutive partition, and all induced tolerance thresholds. Exact rational integration independently checks the expected-error formula; exhaustive partition comparison checks greedy optimality. Separate competing-road examples check route certificates.

From this folder, with MiKTeX or TeX Live installed:

```powershell
pdflatex -interaction=batchmode -halt-on-error chain_compression.tex
pdflatex -interaction=batchmode -halt-on-error chain_compression.tex
```

The figure script uses NumPy and Matplotlib to export the worked example as vector PDF and 300 dpi PNG in `figures/`.
