# Crab pulsar comparison

Calculated November 13, 2026. **No affirmative evidence for the proposed propagation effect emerges from this comparison.** This calculation uses published measurements and limits; it is not a new event-level experiment or a reproduction of the MAGIC likelihood fit.

## Data-access check

Inspected the [MAGIC open-data catalog](https://opendata.magic.pic.es/), the indexed [publication page](https://magic.mpp.mpg.de/backend/publication/show/389), the [paper](https://doi.org/10.3847/1538-4365/aa8404), and its [arXiv full text](https://arxiv.org/html/1709.00346v1). The original pulsar event sample and run-specific response files were not located. Direct requests to the collaboration publication server timed out. This is not proof that the files are unavailable elsewhere or by request.

The catalog does offer [60 hours of Crab Nebula observations](https://zenodo.org/records/11108474); this is a different sample and does not reproduce the original pulsar analysis. It was not substituted for the pulsar dataset. No messages were sent to the authors.

## Recalculated measurements

Section III reports phase differences for two band pairs. Converted using a 33.7 ms period:

| Approximate mean energies | Time difference | Statistical uncertainty | Reported systematic uncertainty | Quadrature uncertainty |
| --- | ---: | ---: | ---: | ---: |
| 75 vs 770 GeV | 175 microseconds | 165 microseconds | 101 microseconds | 194 microseconds |
| 465 vs 770 GeV | 10 microseconds | 263 microseconds | 101 microseconds | 282 microseconds |

The differences also reproduce by subtraction of the individually reported peak phases. The higher-energy comparison is approximately 0.04 Gaussian standard deviations from zero; even the wider-energy comparison is below one. Adding systematics in quadrature is an illustrative approximation, not a new calibrated significance calculation. Both measurements are compatible with zero.

These pairs share their high-energy band and must not be combined as independent measurements. Emission mechanisms can differ between the lower and higher bands. Band mean energies do not specify true second energy moments, so these summary measurements are not used to infer a new quantitative propagation bound.

## Translation of the published bound

The paper's Section III equation (2) uses the same quadratic velocity coefficient convention checked in the LHAASO analysis. Algebraic matching to the minimum-distance paper gives

`EQG2 = sqrt(12) hbar c / Lambda`.

Its Table 6 subluminal profile-likelihood limit, including the reported systematics, is EQG2 > 5.9e10 GeV at 95% confidence. Applying the transformation yields

**Lambda < 1.159e-26 m**, and consequently **k <= Lambda < 1.159e-26 m**, conditional on the model's photon law and the published analysis assumptions.

That length bound is approximately 11.7 times weaker than the LHAASO value translated from 6.9e11 GeV. It is an independent source-class comparison, not a stronger bound. The two published limits have not been combined into a joint confidence interval.

Reported instrumental and astrophysical systematic allowances do not cover arbitrary intrinsic energy-dependent source drifts. Such drifts could imitate or offset a propagation effect. General finite-range lattice models also require the quadratic expansion to hold across the measured energy band.

## Prediction size

Using the nominal distance of 2 kpc and the paper's static propagation equation, Planck spacing with nearest-neighbor interactions predicts approximately **6.50e-23 seconds** between representative energies of 465 and 770 GeV. This is roughly 4e18 times smaller than the simple peak-comparison uncertainty. The distance has an uncertainty of about 0.5 kpc; varying it does not change this sensitivity conclusion.

Using representative band energies illustrates the scale; it is not detector-response integration. The full profile analysis exploits more information than these two peak comparisons, but its bound on Lambda is still about 7e8 Planck lengths.

## Reproduction and artifacts

Run from the workspace root:

```powershell
.venv/Scripts/python.exe -c "from pathlib import Path; import requests; r=requests.get('https://arxiv.org/html/1709.00346v1', timeout=60); r.raise_for_status(); Path('analysis/crab/paper.html').write_bytes(r.content)"
.venv/Scripts/python.exe analysis/crab/analyze_crab.py
```

- `paper.html` and `paper.txt`: local source caches, excluded from Git. The command above retrieves the HTML needed by the script; the plain-text cache is optional.
- `analyze_crab.py`: documented input values, phase subtraction, uncertainty conversion, model predictions and bound transformations.
- `results.json`: complete numeric output, assumptions and limitations.
- `peak_delays.csv`: time differences and uncertainties.
- `peak_comparison.png` and `.pdf`: comparison figure.
- `source_manifest.json`: source hash and access-check outcomes.

The script checks the reported phase differences against subtraction of the source peak values. No new fit, detection claim, or below-Planck geometric conclusion is warranted.
