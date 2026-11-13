# PKS 2155-304 comparison

Completed November 13, 2026. The physical comparison uses the published 2011 timing analysis. The separately downloaded public event archive is used only for a private technical demonstration under its test-release terms, not to make new claims about the source.

## Published timing measurement

H.E.S.S., Astroparticle Physics 34, 738–747 (2011), [DOI](https://doi.org/10.1016/j.astropartphys.2011.01.007), [full text](https://arxiv.org/html/1101.3650v1), analyzed the July 28, 2006 flare. Its final quadratic coefficient is **1.7 +/- 6.3 statistical +/- 6.6 systematic s/TeV^2** (Section 5). The smaller uncertainty visible in its likelihood-curve figure is not the final calibrated error. The final result is consistent with zero.

Adding those errors in quadrature gives 9.12 s/TeV^2, and an illustrative Gaussian significance of 0.19 standard deviations. The corresponding approximate signed 95% interval is [-16.18, 19.58] s/TeV^2. This is a calculation from the reported uncertainties, not a new likelihood fit or confidence-coverage calibration.

The study gives a quadratic energy-scale lower bound of 6.4e10 GeV at 95% confidence. Equations (4)–(5) include the appropriate redshift weighting. Matching that quadratic convention to the minimum-distance model gives EQG2 = sqrt(12) hbar c / Lambda, hence **Lambda < 1.068e-26 m**, and k <= Lambda within the model's assumptions.

The transformed length limit is about 10.8 times weaker than the LHAASO limit previously translated, and about 8% stronger than the Crab length limit. No combined confidence limit has been inferred. Source-dependent intrinsic delays remain a possible nuisance; the geometric distance gap alone does not predict this photon propagation law.

At z = 0.116, using the original paper's cosmology H0 = 2.3e-18 /s and Omega_m = 0.3, the cosmological quadratic kernel is 5.495e16 s. Planck spacing with nearest-neighbor interactions predicts a delay coefficient of 4.61e-17 s/TeV^2, or 7.34e-16 s between 0.25 and 4 TeV. This is far below the reported uncertainty and does not approach a test of Planck spacing.

## Public data and date mismatch

Downloaded the actual [HESS DL3 DR1 archive](https://www.mpi-hd.mpg.de/hfm/HESS/pages/dl3-dr1/): 45,004,800 bytes, SHA-256 `cb0439101300d072e084c255225a863c8dafe1fbf76814ab6188f9b112d7f354`.

The FITS headers and [release notes](https://www.mpi-hd.mpg.de/hfm/HESS/pages/dl3-dr1/hess_dl3_dr1.pdf) identify 15 flare runs from July 29–30, 2006 (OBS_ID 33787–33801), rather than the July 28 sample used for the published LIV fit. Thus this archive cannot reproduce that fit. The original July 28 event-and-response sample was not located in this search. The release is not representative of the best H.E.S.S. reconstruction and does not provide evaluated scientific systematics.

## Technical demonstration on the released events

This is a tool check, not a source result or a new physical constraint. Selected events in good-time intervals, within 0.11 degrees of the catalog source, above the largest run-safe energy threshold (1.0715 TeV) and below 4 TeV. The selection has 1,237 ON events. Five equal-area reflected apertures have 213 OFF events, for a nominal ON-background estimate of 42.6. Original files and their response arrays are retained.

The check measures a centered rank association between arrival time and reconstructed energy within each run. It preserves run identity and permutes energy labels within runs 5,000 times. This prevents between-run acceptance differences from masquerading as a correlation. The observed statistic is 0.00699, with a two-sided permutation diagnostic p = 0.811. Two aperture sensitivity checks also produce unexceptional statistics. Those numbers are saved for software reproducibility only; **they do not establish a source property, measure a propagation lag, or constrain Lambda**.

Within-run detector response and intrinsic spectral evolution are not modeled. Energy dispersion and effective area have not been forward folded. Background events are retained in the rank check. A rank-association null test can have limited power for actual time-shift effects. The published physical limit above is independent of this demonstration.

## Files and reproduction

```powershell
.venv/Scripts/python.exe -c "from pathlib import Path; import requests; r=requests.get('https://arxiv.org/html/1101.3650v1', timeout=60); r.raise_for_status(); Path('analysis/pks2155/paper.html').write_bytes(r.content)"
.venv/Scripts/python.exe analysis/pks2155/download_data.py
.venv/Scripts/python.exe analysis/pks2155/analyze_pks.py
```

Create the root `.venv` and install `requirements.txt` first, as described in the root README. Dependencies include NumPy, SciPy, astropy, matplotlib and requests. The analysis uses the saved `paper.html`; `paper.txt` is an optional readable local copy. Article caches, downloaded archives, and extracted raw data are excluded from Git. The commands above retrieve the required inputs. These commands also rerun the separate software diagnostic under the release terms below; that diagnostic is not part of the companion note's scientific results.

- `results.json`: published-input calculations and separately labeled technical check.
- `run_counts.csv`: selected counts per public run.
- `permutation_null.npy`: technical resampling distribution.
- `association_check.png` and `.pdf`: diagnostic figure.
- `source_manifest.json`: hashes, archive source, and release documentation.
- `dl3/README.txt`: original release terms, preserved verbatim below as well.

## Attribution and original release terms

This work made use of data from the H.E.S.S. DL3 public test data release 1 (HESS DL3 DR1, H.E.S.S. collaboration, 2018).

```text
H.E.S.S. DL3 public test data release 1 (HESS DL3 DR1)
------------------------------------------------------

H.E.S.S. collaboration, 2018

Webpage: https://www.mpi-hd.mpg.de/hfm/HESS/pages/dl3-dr1/

The data and documentation is publicly released by the H.E.S.S. collaboration
as a contribution to the ongoing efforts to define a common open format for
data level 3 of imaging atmospheric Cherenkov telescopes (IACTs) and IACT
open-source science tool development, to enlarge the community involved in
IACT data analysis.

No scientific publications may be derived from the data. Using the data
for new claims about the astrophysical sources is not permitted.

When using this data, please include the following attribution:

    This work made use of data from the H.E.S.S. DL3 public test
    data release 1 (HESS DL3 DR1, H.E.S.S. collaboration, 2018).

Alternatively, use the following shorter version, e.g. for presentations:

    HESS DL3 DR1, H.E.S.S. collaboration

These terms of use must be included in all copies in full or part of the data.

For information on context, aims, use and contacts, as well as a description
of the dataset, see the hess_dl3_dr1.pdf document.
```
