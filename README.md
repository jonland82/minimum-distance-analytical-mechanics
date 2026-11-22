# Consequences of Minimum Distance

What follows if distinct spatial positions are separated by at least a distance `k`? A triangle fits when its shortest side reaches that cutoff. The same threshold lets a routing index answer repeated queries without scanning every candidate stop. A separate physical question starts with waves on a lattice and asks what their dispersion would imply for photon timing.

**[Project website](https://jonland82.github.io/minimum-distance-analytical-mechanics/)** · **[Original paper](consequences_of_minimum_distance.pdf)** · **[Triangle paper](triangle_companion/triangle_exclusion.pdf)** · **[Routing paper](routing_note/one_stop_routing.pdf)** · **[Dynamics note](dynamics_study/dynamics_note.pdf)** · **[Photon-timing companion](companion_note/photon_timing_companion.pdf)**

By Jonathan R. Landers.

## Research threads

- **Geometry.** Uniform discreteness restricts triangles and bisection and makes continuous point trajectories from connected time intervals constant. At every diameter above the cutoff, angle-uniform right triangles have a higher excluded fraction than triangles sampled uniformly by area in normalized side-length coordinates. The mean minimum surviving diameters are infinite and `4k log 2`, respectively.
- **Routing.** Fix the terminals and candidate stops for a one-stop Euclidean route. Sorting by the shortest side of each route triangle and storing prefix minima reduces a cutoff query from linear to logarithmic time after `O(n log n)` preprocessing. At 100,000 synthetic stops and 1,000 queries, the indexed batch was **2.63× faster including construction** than cached exhaustive scans. Every answer agreed.
- **Graph traversal.** Minimum vertex separation `k` and endpoint connection radius `R` bound local degree by `(1 + 2R/k)^2 - 1` in the plane. At fixed `R/k`, edges and graph triangles are linear in the number of vertices, supporting expected linear-time spatial construction and standard sparse-graph routing. The [paper, proofs, reproducible counts, and figures](graph_traversal/README.md) distinguish these consequences from what minimum separation alone permits.
- **Dynamics.** On a one-dimensional lattice with symmetric positive interactions, the leading group-speed reduction is quadratic, with effective length `Lambda >= k`. At the same spacing, stable signed interactions from centered finite-difference formulas suppress dispersion to arbitrarily high order. Phase and group speeds converge to the continuum on fixed bands strictly below the lattice cutoff.
- **Photon timing.** If photons obey the positive-coupling wave law, published LHAASO, MAGIC/Crab, and H.E.S.S./PKS timing limits constrain `Lambda`. The strongest translated bound is about `9.91e-28 m`, roughly 61 million Planck lengths. These limits depend on the propagation model and the assumptions of the observations.

The triangle probabilities depend on how shapes are sampled. The routing proof uses the cutoff for each candidate and holds for arbitrary fixed stops. The wave and timing results depend on the interaction law and the interpretation of the waves as photons.

## Reading and repository map

| Location | Contents |
| --- | --- |
| [Original manuscript](consequences_of_minimum_distance.tex) | Geometry, positive-coupling wave formalism, conditional photon test |
| [Triangle companion](triangle_companion/triangle_exclusion.tex) | Exclusion probabilities, strict ordering, and mean survival thresholds |
| [Routing note](routing_note/one_stop_routing.tex) | Index construction, proof, comparison lower bound, and runtime experiments |
| [Routing implementation](triangle_companion/one_stop.py) | Threshold index and exhaustive baseline |
| [Graph traversal paper](graph_traversal/minimum_separation_traversal.pdf) · [Source and reproduction](graph_traversal/README.md) | Packing bounds, local graph construction, triangle counts, and weighted road illustration |
| [Routing benchmark](routing_note/experiment.py) · [Recorded trials](routing_note/timings.csv) · [Runtime plots](routing_note/runtime.pdf) | Synthetic workloads, timing data, and build-cost crossover |
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

Run the routing experiment and regenerate its figures from the repository root:

```powershell
.venv/Scripts/python.exe -m routing_note.experiment
.venv/Scripts/python.exe -m routing_note.figures
```

The experiment writes fresh measurements to `routing_note/timings.csv`. Run just the figure command to reproduce the plots from the recorded trials.

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
