# How closely can a discrete space imitate continuum waves?

**Question:** if there is a minimum distance, must waves reveal it? The original paper suggested a possible route to detection: a small change in wave speed could accumulate over an astronomical journey. This note asks whether that change follows from the spacing itself or from the interactions placed on the lattice.

**Result:** at fixed lattice spacing, stable signed interactions can approximate continuum phase and group speeds arbitrarily well on any fixed wave-number band strictly below the lattice cutoff. Minimum spacing alone therefore does not enforce the earlier quadratic slowdown. Positive pair interactions do enforce a stronger limitation.

Read [the mathematical note](dynamics_note.pdf) or [its LaTeX source](dynamics_note.tex).

The note follows the question from the [original geometric premise](../consequences_of_minimum_distance.pdf) and [photon-timing tests](../companion_note/photon_timing_companion.pdf), through the limitation of positive interactions, a stable signed construction, numerical comparisons, and the differences that remain at finite range and at the cutoff. It closes by identifying what a physical model must specify before an experiment can test its predicted signal. Definitions and a range-two cancellation example introduce the formalism; proofs and numerical results retain their original scope.

## What was done

- Proved that, at fixed long-wavelength speed, nearest-neighbor interactions maximize phase speed pointwise among all symmetric positive finite-range couplings.
- Constructed a stable signed family from standard centered finite-difference rules. Range R cancels the leading dispersion errors through order 2R, so group-speed error begins at order (qk)^(2R).
- Proved stability through a positive polynomial/energy representation, and proved group speed stays between zero and c for this family. Stability is a global statement, not inferred from a sampled grid.
- Compared ranges 1–16 on bands ending at pi/4, pi/2 and 3pi/4.
- Optimized squared phase-speed error in a stability-certified signed subclass using a sampled linear program, then checked a dense independent grid and refined candidate extrema. This is not a proof of the continuous optimum over all stable rules.
- Identified remaining restrictions: no fixed finite-range rule has exact continuum dispersion on an open interval; a nonzero-frequency zone-edge mode has zero group speed. An infinite-range signed kernel can reproduce continuum dispersion exactly inside the Brillouin zone, illustrating the role of locality.

These are numerical/mathematical model studies, not synthetic observations used to validate nature. The finite-difference formulas are standard; the purpose is to clarify their implications when interpreted as candidate dynamics on discrete positions.

## Representative results

For 0 <= qk <= pi/2 (wavelengths >= 4 lattice spacings):

| Model | Maximum phase-speed error | Maximum group-speed error |
| --- | ---: | ---: |
| Nearest neighbor | 9.97% | 29.3% |
| Centered, range 4 | 0.337% | 2.66% |
| Centered, range 16 | 0.0000146% | 0.000395% |
| Band-optimized, range 4 | 0.00668% | 0.359% |

All errors are relative to c. The optimized family minimizes squared phase error, not group error. The range-four optimized rule has a maximum full-zone group speed about 1.00073 c, despite global energy stability. The centered family obeys the group-speed cap. Neither a group-speed cap nor energy stability implies a strict causal front or a complete relativistic theory.

## Reproduce

From the workspace root:

```powershell
python dynamics_study/study.py
python dynamics_study/validate.py
```

Requires NumPy, SciPy, SymPy, mpmath and matplotlib. No network access or physical dataset is required. The script uses exact rational and symbolic checks, dense numerical validation, and 70-digit endpoint calculations for centered rules.

To build the PDF from this folder:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error dynamics_note.tex
pdflatex -interaction=nonstopmode -halt-on-error dynamics_note.tex
```

## Files

- `study.py`: construction, optimization, exact checks and plotting.
- `results.json`: coefficients, errors, solver scope and certificate outcomes.
- `errors.csv`: compact numerical comparison.
- `validate.py` and `verification.json`: independent matrix-spectrum, numerical-derivative and asymptotic-coefficient checks.
- `error_table.tex`: generated table used by the note.
- `figures/dispersion.*`: full-zone phase and group speeds.
- `figures/convergence.*`: improvement with interaction range.
- `figures/optimized.*`: phase/group tradeoff in band optimization.

## Interpretation

The earlier astronomical bounds retain their stated applicability to the positive-coupling quadratic model. They cannot be promoted to universal tests of every stable discrete geometry. Signed rules can have a vanishing or negative fourth moment, so that quantity cannot always be called a squared effective length. Choosing which couplings are physically allowed requires additional physics. These results do not establish that photons follow any of the candidate dynamics.

References are included in the note: NIST DLMF 3.4, Fornberg (1988), and Trefethen (2000).
