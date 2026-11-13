"""Recalculate published Crab peak summaries and translate the MAGIC bound.

No event data or likelihood curve is fitted. Source: Ahnen et al. (2017),
ApJS 232, 9, https://doi.org/10.3847/1538-4365/aa8404.
"""
from pathlib import Path
import json
import hashlib
import numpy as np
from scipy.constants import c, hbar, G, electron_volt, parsec
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent
SOURCE='https://arxiv.org/html/1709.00346v1'
HBARC=hbar*c/(1e9*electron_volt)  # GeV m
LP=np.sqrt(hbar*G/c**3)
DISTANCE=2000*parsec
PERIOD=.0337

def delay(length, eh, el):
    return DISTANCE/c*length**2*(eh**2-el**2)/(8*HBARC**2)

# Section III gives more precise phases than the rounded Table 1 entries.
phase=np.array([.3983,.4032,.4035])
phase_stat=np.array([.0013,.0063,.0047])
energies=np.array([75.,465.,770.])
pairs=[]
for lo,reported,stat in [(0,.0052,.0049),(1,.0003,.0078)]:
    syst=.003
    sigma=np.hypot(stat,syst)
    reconstructed=phase[2]-phase[lo]
    reconstructed_stat=np.hypot(phase_stat[2],phase_stat[lo])
    assert abs(reconstructed-reported)<1e-12
    assert abs(reconstructed_stat-stat)<.0001
    pairs.append(dict(
        comparison='55-100 vs 600-1200 GeV' if lo==0 else '400-600 vs 600-1200 GeV',
        mean_low_GeV=float(energies[lo]),mean_high_GeV=770.,
        reported_phase_difference=reported,
        phase_difference_recalculated_from_peaks=float(reconstructed),
        statistical_phase_error=stat,systematic_phase_error=syst,
        quadrature_phase_error=float(sigma),
        lag_s=reported*PERIOD,statistical_lag_error_s=stat*PERIOD,
        systematic_lag_error_s=syst*PERIOD,
        quadrature_lag_error_s=float(sigma*PERIOD),
        illustrative_gaussian_z=float(reported/sigma),
        illustrative_two_sided_gaussian_p=float(2*norm.sf(abs(reported/sigma))),
        approximate_signed_lag_interval_95_s=[float((reported-1.96*sigma)*PERIOD),
                                               float((reported+1.96*sigma)*PERIOD)],
        Planck_nearest_neighbor_delay_s=delay(LP,770,energies[lo]),
    ))

bounds=[]
for method,scale in [('Peak comparison: 75 vs 770 GeV',1.8e10),
                     ('Peak comparison: 465 vs 770 GeV',1.4e10),
                     ('Profile likelihood: statistical only',8e10),
                     ('Profile likelihood: including reported systematics',5.9e10)]:
    lam=np.sqrt(12)*HBARC/scale
    bounds.append(dict(method=method,published_confidence=.95,
                       EQG2_lower_GeV=scale,Lambda_upper_m=float(lam),
                       Lambda_upper_Planck_lengths=float(lam/LP),
                       predicted_delay_at_bound_770_vs_465_s=delay(lam,770,465)))

official=bounds[-1]['Lambda_upper_m']
for p in pairs:
    p['delay_at_published_profile_bound_s']=delay(official,p['mean_high_GeV'],p['mean_low_GeV'])
lhaaso=json.loads((OUT.parent/'translated_bounds.json').read_text())
lhaaso_lam=lhaaso['translated_published_results'][1]['Lambda_upper_m_from_rounded_EQG']
results=dict(
    source=SOURCE,published_doi='10.3847/1538-4365/aa8404',
    analysis_date='2026-11-13',event_level_fit_performed=False,
    calculation='Recalculation of reported peak differences and algebraic translation of published bounds',
    constants=dict(period_s=PERIOD,distance_kpc=2.,distance_uncertainty_kpc=.5,
                   hbar_c_GeV_m=HBARC,Planck_length_m=float(LP)),
    peak_inputs=dict(mean_energies_GeV=energies.tolist(),phases=phase.tolist(),
                     statistical_phase_errors=phase_stat.tolist(),
                     location_in_source='Section III; phase differences immediately preceding Table 2'),
    peak_comparisons=pairs,translated_published_bounds=bounds,
    official_length_bound_relative_to_LHAASO=float(official/lhaaso_lam),
    limitations=['No original MAGIC event sample or run-specific detector response located for this study',
                 'No independent peak fit or calibrated profile-likelihood reproduction',
                 'Quadrature treatment of reported systematic error is illustrative, not a new coverage calibration',
                 'Source phase changes are degenerate with propagation delays',
                 'Energy-band means do not fix true second energy moments; no new bound is inferred from them',
                 'Reported systematics do not include arbitrary intrinsic energy-dependent source drift',
                 'Published bound inherits source, detector and quadratic-regime assumptions',
                 'Published limits are not combined with LHAASO into a joint confidence limit'],
)
(OUT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
np.savetxt(OUT/'peak_delays.csv',np.array([[p['mean_low_GeV'],p['mean_high_GeV'],p['lag_s'],
    p['statistical_lag_error_s'],p['systematic_lag_error_s'],p['quadrature_lag_error_s'],
    p['Planck_nearest_neighbor_delay_s']] for p in pairs]),delimiter=',',
    header='mean_low_GeV,mean_high_GeV,lag_s,stat_error_s,sys_error_s,quadrature_error_s,Planck_prediction_s',comments='')
fig,ax=plt.subplots(figsize=(7.6,4.8))
x=np.arange(2)
ax.errorbar(x,[p['lag_s']*1e6 for p in pairs],
    yerr=[p['quadrature_lag_error_s']*1e6 for p in pairs],fmt='o',capsize=4,
    label='Published peak differences; errors combined in quadrature')
ax.scatter(x+.08,[p['delay_at_published_profile_bound_s']*1e6 for p in pairs],
    marker='s',label='Prediction at published profile length bound')
ax.axhline(0,color='black',lw=1,label='Zero delay; Planck prediction indistinguishable at this scale')
ax.set_xticks(x,['75 vs 770 GeV','465 vs 770 GeV'])
ax.set(xlabel='Approximate mean photon energies',ylabel='Higher-energy lag (microseconds)',
       title='Crab pulsar: recalculation from published peak measurements')
ax.legend(fontsize=7,loc='upper right');ax.grid(alpha=.2)
fig.text(.5,.01,'Published measurements, not a new event fit. Full profile limit uses additional event information.',
         ha='center',fontsize=8)
fig.tight_layout(rect=(0,.04,1,1))
fig.savefig(OUT/'peak_comparison.png',dpi=180);fig.savefig(OUT/'peak_comparison.pdf')
manifest=dict(source=SOURCE,sha256_paper_html=hashlib.sha256((OUT/'paper.html').read_bytes()).hexdigest(),
    raw_event_data_downloaded=False,
    access_checks=[dict(url='https://magic.mpp.mpg.de/backend/publication/show/389',
                       result='Indexed publication metadata found; direct local request timed out'),
                   dict(url='https://opendata.magic.pic.es/',
                       result='Public catalog inspected; original pulsar LIV sample not listed'),
                   dict(url='https://zenodo.org/records/11108474',
                       result='60-hour Crab Nebula release identified; not the original full pulsar LIV sample'),
                   dict(url='https://doi.org/10.3847/1538-4365/aa8404',
                       result='Published measurements available through indexed text and arXiv full text')])
(OUT/'source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
