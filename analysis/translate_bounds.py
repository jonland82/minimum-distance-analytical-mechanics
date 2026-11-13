"""Translate published LHAASO bounds; this script does not fit event data."""
import json
from pathlib import Path
import numpy as np
from scipy.constants import c, hbar, electron_volt, G
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
HBARC = hbar*c/(1e9*electron_volt)  # GeV m
LP = np.sqrt(hbar*G/c**3)
EPL = HBARC/LP
H0 = 67.36*1000/(1e6*3.085677581491367e16)
Z, OM = 0.151, 0.315
K2 = quad(lambda z: (1+z)**2/(H0*np.sqrt(OM*(1+z)**3+1-OM)), 0, Z)[0]

def length_from_scale(eqg):
    return np.sqrt(12)*HBARC/eqg

def length_from_eta(eta):
    return LP*np.sqrt(12e15*eta)

def delay(length, eh_tev, el_tev=0):
    return K2*length**2*((eh_tev*1000)**2-(el_tev*1000)**2)/(8*HBARC**2)

rows = []
for name, eta_bf, eta_lo, eta_hi, eqg in [
    ('CCF', .25, -.47, .66, 4.7e11),
    ('ML MINOS', .01, -.31, .32, 6.9e11),
    ('ML calibrated', None, -.30, .29, 7.2e11),
]:
    lam = length_from_eta(eta_hi)
    rows.append(dict(method=name, eta2_best_fit=eta_bf,
                     eta2_interval_95=[eta_lo,eta_hi],
                     published_EQG2_lower_GeV=eqg,
                     Lambda_upper_m_from_eta=lam,
                     Lambda_upper_m_from_rounded_EQG=length_from_scale(eqg),
                     Lambda_upper_in_Planck_lengths=lam/LP,
                     delay_1TeV_vs_0_upper_s=delay(lam,1),
                     delay_7TeV_vs_0_upper_s=delay(lam,7)))
results = dict(
    independent_event_fit=False,
    method='Algebraic translation of published Table I confidence intervals; no new statistical inference',
    source='https://doi.org/10.1103/PhysRevLett.133.071501',
    formulas=dict(EQG2='sqrt(12) hbar c / Lambda',
                  eta2='1e-15 (Lambda/lP)^2 / 12',
                  delay='K2 Lambda^2 (Eh^2-El^2) / (8 (hbar c)^2)'),
    assumptions=['Quadratic low-energy regime', 'Photon group velocity follows the paper',
                 'Constant physical Lambda in cosmological frame',
                 'Same source and detector assumptions as the published intervals',
                 'For general finite-range models the expansion must hold throughout the measured band'],
    constants=dict(hbar_c_GeV_m=HBARC, Planck_length_m=LP, Planck_energy_GeV=EPL,
                   redshift=Z,H0_km_s_Mpc=67.36,Omega_m=OM,K2_s=K2),
    translated_published_results=rows,
    Planck_nearest_neighbor=dict(eta2=1e-15/12,
        delay_1TeV_vs_0_s=delay(LP,1),delay_7TeV_vs_0_s=delay(LP,7),
        delay_7TeV_vs_0point2_s=delay(LP,7,.2)),
)
(OUT/'translated_bounds.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
fig, ax = plt.subplots(figsize=(7.5,4.5))
e = np.geomspace(.2,7,200)
ax.loglog(e,[delay(LP,x,.2) for x in e],label='Planck spacing; nearest neighbors')
ax.loglog(e,[delay(rows[1]['Lambda_upper_m_from_eta'],x,.2) for x in e],
          label='Length at published 95% ML upper bound')
ax.set(xlabel='Observed photon energy (TeV)',ylabel='Delay relative to 0.2 TeV (s)',
       title='GRB 221009A: model predictions at z = 0.151')
ax.grid(True,which='both',alpha=.25)
ax.legend(fontsize=8)
fig.text(.5,.01,'Predictions and translated published bound; no independent event fit.',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.04,1,1))
fig.savefig(OUT/'delay_comparison.png',dpi=180)
fig.savefig(OUT/'delay_comparison.pdf')
print(json.dumps(results,indent=2))
