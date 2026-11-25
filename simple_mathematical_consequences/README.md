# How finely can we measure a curve?

[Read the extended note](arc_length_note.pdf) · [LaTeX source](arc_length_note.tex)

A self-contained progression from the parabola and its arc-length integral to
polygonal approximation, a minimum-distance restriction on the triangles, and
the resulting error. The maximum triangle count is exact for the stated uniform
construction; the general count formula is an upper bound. The note distinguishes
these claims from optimization over other placements or estimators.

The paper has two numbered sections with inline bold subsection titles ending in periods. The Main Result section develops the adjacent-angle stability theorem,
including its full proof, equality case, explicit estimator, combined length
certificate, and disjoint-pair extension. A second figure compares certificates
for a quartic family, including the exact parabola case. The theorem assumes an
independent bound on the second derivative. Priority for the precise inequality
remains open. Its source is `main_result.tex`, included by the main manuscript.

Coordinates and the cutoff are dimensionless in a fixed length unit. The physical
interpretation, admissible vertices, parity restriction, error bound, and small-cutoff
asymptotic are stated explicitly. Two repository geometry papers provide context;
the derivations do not depend on reading them.

From the repository root, regenerate the figure and numerical table:

```powershell
python simple_mathematical_consequences/prepare.py
```

The script also checks the count by enumerating uniform partitions, verifies all
pairwise vertex separations for the table examples, compares the arc integral with
Gaussian quadrature, and checks the error bound and leading coefficient.
It also checks the angular certificates against independent numerical integration
and regenerates the second figure.
It requires NumPy and Matplotlib.

From this folder, build the PDF with MiKTeX or TeX Live:

```powershell
pdflatex -interaction=batchmode -halt-on-error arc_length_note.tex
pdflatex -interaction=batchmode -halt-on-error arc_length_note.tex
```
