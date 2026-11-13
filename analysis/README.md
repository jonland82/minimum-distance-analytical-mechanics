# GRB 221009A: preliminary test of the photon-delay model

Analysis date: November 13, 2026.

Subsequent mathematical study: [How closely can a discrete space imitate continuum waves?](../dynamics_study/README.md). Stable signed interactions can suppress the leading dispersion to arbitrarily high order; the study distinguishes this from the positive-coupling class constrained by the observations below.

Companion note: [Photon-Timing Tests of a Minimum-Distance Propagation Model](../companion_note/photon_timing_companion.pdf), with [LaTeX source and build instructions](../companion_note/README.md). It reviews the formalism, the three observational comparisons, and the sensitivity required for the Planck-spacing benchmark.

Additional comparison completed: [PKS 2155-304 / H.E.S.S.](pks2155/README.md). The published quadratic coefficient is consistent with zero and translates to Lambda < 1.07e-26 m. Downloaded public event data are from later nights and carry test-release restrictions; a separate private software diagnostic is saved, without deriving a new scientific limit or reproducing the published fit.

Additional comparison completed: [Crab pulsar](crab/README.md). Recalculation of published pulse-position summaries is consistent with zero delay; translating the published MAGIC bound gives Lambda < 1.16e-26 m. The original pulsar event-and-response sample was not located, so this is a published-summary calculation, not a new event fit. Scripts, numeric results, provenance and a plot are saved in `crab/`.

**Finding:** the released WCDA counts show weak energy-dependent timing structure, but this preliminary analysis does not establish a propagation effect. Translating the collaboration's corrected result gives an effective interaction length below roughly 10^-27 m. Planck spacing with nearest-neighbor interactions remains far below this sensitivity.

## Data and scope

Downloaded the actual 72,331,727-byte archive linked by the [National High Energy Physics Science Data Center](https://www.nhepsdc.cn/resource/astro/lhaaso/paper-PRL2024-133071501), dataset DOI [10.12402/opendata/LHAASO/20240829100037](https://doi.org/10.12402/opendata/LHAASO/20240829100037). SHA-256: `9f694d18c5e2f65562c6f841c500361385bee6351e45544c5a368d7e79c10644`.

The archive contains ON/OFF event trees and light curves, plus simulated time-energy distributions for three EBL attenuation assumptions. The stored folder name has a legacy ZIP encoding; the scripts locate files by basename. No supplied executable code was run.

The independent calculation here is a cross-correlation diagnostic. The response-corrected maximum-likelihood fit and its shuffling calibration have **not** been independently reproduced. Published confidence bounds below retain the collaboration's statistical and source assumptions.

## Independent timing calculation

Used all ten `h1d_on_nq03t30_*` and `h1d_bk_nq03t30_*` histograms in `light_curve.root`, 232–400 seconds after the burst trigger, with 0.1-second bins. There are 54,767 ON counts and 12,107.75 estimated background counts in this interval. OFF counts are stored at one-quarter their original exposure counts, consistent with the ROOT metadata.

Calculated background-subtracted cross-correlations against the lowest-energy channel and fitted a Gaussian plus constant to each peak over a fixed +/-10-second lag interval. Positive lag means the higher channel arrives later. Used 500 joint Poisson resamples (seed 221009), resampling ON and OFF counts and retaining the covariance induced by the shared reference channel.

The highest channel (median energy 1.601 TeV) has a lag of 0.936 +/- 0.431 seconds relative to the lowest (median 0.354 TeV). Changing the peak-fit interval to +/-8 or +/-15 seconds changes this estimate to 0.752 or 1.148 seconds. This estimator dependence is material compared with the statistical error.

A diagnostic regression against squared median energies gives an **uncorrected** eta2 of 0.502 +/- 0.199. It omits the broad, overlapping true-energy distributions and spectral-evolution correction and must not be read as evidence for quantum gravity or used to set a propagation-only bound. A zero-lag omnibus statistic is approximately chi-square 14.69 for nine channels (p = 0.10); this is an approximate check, not a calibrated test of the physical model. Source emission lags can also contribute.

The lag CSV and full covariance/bootstrap results are in `measured_lags.csv` and `ccf_results.json`; the figure is `measured_lags.png` (also PDF).

## Translation into the paper's parameters

For the quadratic subluminal convention, matching the leading velocity coefficients gives

`EQG2 = sqrt(12) hbar c / Lambda`

and, using the collaboration's parameter,

`eta2 = 10^-15 (Lambda/lP)^2 / 12`.

The [published collaboration analysis, Table I](https://doi.org/10.1103/PhysRevLett.133.071501) gives a bias-corrected maximum-likelihood best fit eta2 = 0.01 with a 95% interval [-0.31, 0.32]. Its upper endpoint translates to Lambda < 1.002e-27 m. The calibrated endpoint 0.29 gives 9.535e-28 m. Rounded published EQG2 values lead to percent-level differences. These are transformed published intervals, not independently calculated confidence limits. The interval includes zero; a small positive best fit is not a detection. The source reports an uncorrected ML value 0.20 and estimated bias 0.19, illustrating the importance of calibration.

Within the paper's positive-coupling model, k <= Lambda, so the same upper bound also limits k. For nearest neighbors k = Lambda. General finite-range models require the low-energy expansion to be valid over the measured band; arbitrary very long interaction ranges are not automatically covered by a quadratic truncation.

Numerically integrated the cosmological kernel at z = 0.151 using H0 = 67.36 km/s/Mpc and Omega_m = 0.315:

`K2 = integral (1+z)^2/H(z) dz = 7.70778e16 seconds`.

For Lambda = lP, the predicted 7 TeV versus 0.2 TeV delay is 3.165e-15 seconds. For Lambda at the transformed ML upper endpoint, it is about 12.15 seconds. This latter number illustrates the model coefficient at the interval endpoint; it is not a measured lag between the highest and lowest WCDA channels (whose median energies are much closer and whose responses overlap). The bound on Lambda is approximately 62 million Planck lengths, or about 3.8e15 times the Planck nearest-neighbor delay coefficient.

Assumptions: photons obey the paper's propagation law; Lambda is a constant physical length in the cosmological rest frame; the quadratic expansion applies; the observational source, spectrum, background and detector assumptions are applicable. These observations do not directly test the discrete-geometry propositions or exclude Planck spacing.

## Reproduction

From the workspace root in PowerShell:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe analysis/download_data.py
.venv/Scripts/python.exe analysis/translate_bounds.py
.venv/Scripts/python.exe analysis/fit_ccf.py
```

Dependencies are listed in the root `requirements.txt`. On macOS/Linux, use `.venv/bin/python`. Raw archives and extracted data are downloaded locally and excluded from Git. `translated_bounds.json` contains the constants, cosmological integral, transformations and predicted delays. `archive_manifest.json` records the downloaded files and checksum.
