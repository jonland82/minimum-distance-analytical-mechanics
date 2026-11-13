# Photon-Timing Tests of a Minimum-Distance Propagation Model

Companion to `../consequences_of_minimum_distance.tex`.

Read [the PDF](photon_timing_companion.pdf) or edit [the LaTeX source](photon_timing_companion.tex).

The note reviews the geometry-to-dynamics assumptions, derives the effective length and photon-delay conversion, presents the LHAASO, MAGIC/Crab and H.E.S.S./PKS comparisons, and discusses their physical meaning and sensitivity limits. It defers the interacting photon–matter extension to later work.

The scientific conclusions distinguish the independent exploratory LHAASO diagnostic from the published confidence limits, the Crab summary calculation from an event fit, and the published PKS result from later-night public test files. No numerical results or figures derived from the restricted HESS DR1 archive are presented as scientific findings in the note. No new joint confidence limit or affirmative evidence for minimum-distance geometry is claimed.

## Build

From this folder in PowerShell:

```powershell
python prepare_results.py
pdflatex -interaction=nonstopmode -halt-on-error photon_timing_companion.tex
pdflatex -interaction=nonstopmode -halt-on-error photon_timing_companion.tex
```

`prepare_results.py` needs NumPy and matplotlib. It reads the existing analysis JSON files and generates `numbers.tex`, `results_table.tex`, the comparison figure, and `provenance.json` with input hashes. It does not download data or rerun inference. The LaTeX document requires the packages used by the original manuscript plus `graphicx` and `caption`.

The comparison table consistently uses the rounded published energy-scale limits before transforming them, rather than mixing those with bounds calculated from rounded fitted-parameter endpoints. The prose explains the small difference for LHAASO. The sensitivity scaling is derived in the note and marked as idealized.

## Subsequent dynamics study

The [dynamics note](../dynamics_study/README.md) keeps the lattice spacing fixed and relaxes positivity of pair couplings while retaining stability. Standard centered signed rules can cancel the leading quadratic slowdown and approximate continuum waves on bands strictly below the cutoff. The limits in this companion retain their applicability to the stated positive-coupling model; they are not universal bounds on all stable minimum-distance dynamics.
