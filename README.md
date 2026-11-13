# Consequences of Minimum Distance

What follows if distinct spatial positions are separated by at least a distance `k`? This project follows that premise from elementary geometry through lattice dynamics to conditional astronomical tests, then studies how changing the interactions changes the predictions.

**[Project website](https://jonland82.github.io/minimum-distance-analytical-mechanics/)** · **[Original paper](consequences_of_minimum_distance.pdf)** · **[Experimental companion](companion_note/photon_timing_companion.pdf)** · **[Dynamics note](dynamics_study/dynamics_note.pdf)**

By Jonathan Robert Landers. Current notes and calculations: November 13, 2026.

## Findings

- Uniform discreteness restricts Euclidean triangles and bisection, and prevents nonconstant continuous point trajectories from connected time intervals.
- On an additional one-dimensional lattice model with symmetric positive interactions, the leading group-speed reduction is quadratic, with effective length `Lambda >= k`.
- If photons obey this law, published LHAASO, MAGIC/Crab, and H.E.S.S./PKS timing limits constrain `Lambda`. The strongest translated bound here is about `9.91e-28 m`, roughly 61 million Planck lengths. No positive propagation evidence or below-Planck geometric conclusion is established.
- Minimum distance alone does **not** enforce this slowdown. At the same spacing, stable signed interactions from standard centered finite-difference formulas suppress dispersion to arbitrarily high order. Phase and group speeds converge to the continuum on fixed bands strictly below the lattice cutoff as interaction range grows.

The geometric hypothesis, the lattice dynamics, and the interpretation as photon propagation are distinct assumptions. This is an expository and computational exploration, not a verified theory of quantum gravity or a claim that the finite-difference formulas are new.

## Reading and repository map

| Location | Contents |
| --- | --- |
| [Original manuscript](consequences_of_minimum_distance.tex) | Geometry, positive-coupling wave formalism, conditional photon test |
| [Experimental companion](companion_note/README.md) | Formalism, three observational comparisons, sensitivity requirements |
| [LHAASO analysis](analysis/README.md) | Independent exploratory cross-correlation, transformed published limits, provenance |
| [Crab comparison](analysis/crab/README.md) | Published pulse-summary recalculation; no original event-level fit |
| [PKS comparison](analysis/pks2155/README.md) | Published-result translation; separate restricted-release software diagnostic |
| [Dynamics study](dynamics_study/README.md) | Proofs, stable signed constructions, optimization, independent numerical checks |
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
