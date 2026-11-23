# Consequences of Minimum Distance

What follows if distinct spatial positions are separated by at least a distance `k`? A triangle fits when its shortest side reaches that cutoff. A related routing question asks how compactly we can summarize road costs as a minimum edge charge changes. A separate physical question starts with waves on a lattice and asks what their dispersion would imply for photon timing.

**[Project website](https://jonland82.github.io/minimum-distance-analytical-mechanics/)** · **[Original paper](consequences_of_minimum_distance.pdf)** · **[Triangle paper](triangle_companion/triangle_exclusion.pdf)** · ? **[Compact road shortcuts](variable_floor_compression/chain_compression.pdf)** · **[Dynamics note](dynamics_study/dynamics_note.pdf)** · **[Photon-timing companion](companion_note/photon_timing_companion.pdf)**

By Jonathan R. Landers.

## Research threads

- **Geometry.** Uniform discreteness restricts triangles and bisection and makes continuous point trajectories from connected time intervals constant. At every diameter above the cutoff, angle-uniform right triangles have a higher excluded fraction than triangles sampled uniformly by area in normalized side-length coordinates. The mean minimum surviving diameters are infinite and `4k log 2`, respectively.
- **Graph traversal.** Minimum vertex separation `k` and endpoint connection radius `R` bound local degree by `(1 + 2R/k)^2 - 1` in the plane. At fixed `R/k`, edges and graph triangles are linear in the number of vertices, supporting expected linear-time spatial construction and standard sparse-graph routing. The [paper, proofs, reproducible counts, and figures](graph_traversal/README.md) distinguish these consequences from what minimum separation alone permits.
- **Chain compression.** When every edge is charged at least `k`, consecutive groups of sorted edge costs give compact shortcut summaries. Exact worst-case and average-error identities support optimal grouping for a chosen uniform tolerance and an additive certificate for the returned route. The [five-page note and reproducible figure](variable_floor_compression/README.md) include proofs and exact-arithmetic checks.
- **Dynamics.** On a one-dimensional lattice with symmetric positive interactions, the leading group-speed reduction is quadratic, with effective length `Lambda >= k`. At the same spacing, stable signed interactions from centered finite-difference formulas suppress dispersion to arbitrarily high order. Phase and group speeds converge to the continuum on fixed bands strictly below the lattice cutoff.
- **Photon timing.** If photons obey the positive-coupling wave law, published LHAASO, MAGIC/Crab, and H.E.S.S./PKS timing limits constrain `Lambda`. The strongest translated bound is about `9.91e-28 m`, roughly 61 million Planck lengths. These limits depend on the propagation model and the assumptions of the observations.

The triangle probabilities depend on how shapes are sampled. The wave and timing results depend on the interaction law and the interpretation of the waves as photons.

## Reading and repository map

| Location | Contents |
| --- | --- |
| [Original manuscript](consequences_of_minimum_distance.tex) | Geometry, positive-coupling wave formalism, conditional photon test |
| [Triangle companion](triangle_companion/triangle_exclusion.tex) | Exclusion probabilities, strict ordering, and mean survival thresholds |
| [Compact Road Shortcuts with Guaranteed Error](variable_floor_compression/chain_compression.pdf) · [Source and checks](variable_floor_compression/README.md) | Five-page derivation of exact shortcut errors, optimal consecutive grouping, and route certificates |
| [Graph traversal paper](graph_traversal/minimum_separation_traversal.pdf) · [Source and reproduction](graph_traversal/README.md) | Packing bounds, local graph construction, triangle counts, and weighted road illustration |
| [Experimental companion](companion_note/README.md) | Formalism, three observational comparisons, sensitivity requirements |
| [LHAASO analysis](analysis/README.md) | Independent exploratory cross-correlation, transformed published limits, provenance |
| [Crab comparison](analysis/crab/README.md) | Published pulse-summary recalculation; no original event-level fit |
| [PKS comparison](analysis/pks2155/README.md) | Published-result translation; separate restricted-release software diagnostic |
| [Dynamics study](dynamics_study/README.md) | Must minimum distance leave a wave signature? Positive and signed interactions, proofs, optimization, and independent checks |
| [Scale reach](analysis/scale_reach.md) | Sensitivity context and model dependence |
| `index.html`, `site.css`, `site.js` | Static project page and interactive centered-family group-speed plot |

The observational limits are separate transformations of published confidence bounds; there is no joint confidence interval. The independent LHAASO diagnostic does not reproduce the collaboration's calibrated likelihood analysis. The public H.E.S.S. test release covers different nights from its published timing fit and is not used for new source claims. Its original terms and attribution are retained in the [PKS documentation](analysis/pks2155/README.md#attribution-and-original-release-terms).

## Reproduce

Use Python 3.12 or later. Create a local environment and install dependencies:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

On macOS/Linux, replace `.venv/Scripts/python.exe` with `.venv/bin/python`.

The mathematical study needs no downloaded data:

```powershell
.venv/Scripts/python.exe dynamics_study/study.py
.venv/Scripts/python.exe dynamics_study/validate.py
```

`study.py` regenerates coefficients, error tables, and figures. `validate.py` independently checks matrix spectra, derivatives, and asymptotic coefficients. The saved verification records 18 passing checks. This verifies the implemented model, not its description of nature.

For the LHAASO diagnostic and bound conversions:

```powershell
.venv/Scripts/python.exe analysis/download_data.py
.venv/Scripts/python.exe analysis/translate_bounds.py
.venv/Scripts/python.exe analysis/fit_ccf.py
```

The download is approximately 72 MB. See each analysis README for assumptions, input details, and commands for the Crab and PKS comparisons. External archives, extracted raw data, cached articles, local environments, and build intermediates are excluded from Git; scripts, saved numerical results, finished figures, PDFs, and source manuscripts are included. Source-document caches required by the Crab/PKS scripts can be retrieved with the commands in their READMEs.

To regenerate the companion's tables and figure from saved results:

```powershell
.venv/Scripts/python.exe companion_note/prepare_results.py
```

Build each PDF with `pdflatex` twice from the directory containing its `.tex` file. Build the original manuscript from the repository root. MiKTeX or TeX Live supplies the required LaTeX packages. Subfolder READMEs contain the exact build commands.

## Website

The static page is published with GitHub Pages from `/` on `master`. There is no Node build step. To preview locally, run `python -m http.server 8000` from the root and open `http://localhost:8000`. MathJax is loaded from jsDelivr to render equations; the interactive plot uses local JavaScript and the same centered-family polynomial as the dynamics study.

The visual style follows [Sorting as Gradient Flow](https://jonland82.github.io/sorting-as-gradient-flow/), another project by the author.
