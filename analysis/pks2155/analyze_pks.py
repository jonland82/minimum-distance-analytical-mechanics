"""PKS 2155-304: published-bound translation and separate public-event diagnostic.

The public archive is July 29-30, not the July 28 sample of the 2011 LIV paper.
An energy-time rank association is not a fitted propagation delay.
"""
from pathlib import Path
import json, hashlib
import numpy as np
from scipy.constants import hbar,c,G,electron_volt
from scipy.integrate import quad
from scipy.stats import rankdata
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent
ROOT=OUT/'dl3'
HC=hbar*c/(1e9*electron_volt)
LP=np.sqrt(hbar*G/c**3)
K=quad(lambda z:(1+z)**2/(2.3e-18*np.sqrt(.3*(1+z)**3+.7)),0,.116)[0]
scale=6.4e10
lam=np.sqrt(12)*HC/scale
tau,sstat,ssys=1.7,6.3,6.6
sigma=np.hypot(sstat,ssys)
published=dict(event_fit_reproduced=False,redshift=.116,
    source='https://arxiv.org/html/1101.3650v1',
    source_doi='10.1016/j.astropartphys.2011.01.007',
    quadratic_coefficient_s_TeV2=tau,statistical_error_s_TeV2=sstat,
    systematic_error_s_TeV2=ssys,quadrature_error_s_TeV2=float(sigma),
    illustrative_gaussian_z=float(tau/sigma),
    approximate_gaussian_interval95_s_TeV2=[float(tau-1.96*sigma),float(tau+1.96*sigma)],
    confidence95_EQG2_lower_GeV=scale,Lambda_upper_m=float(lam),
    Lambda_upper_Planck_lengths=float(lam/LP),
    cosmology=dict(H0_s_inverse=2.3e-18,Omega_m=.3,K2_s=K),
    Planck_nearest_neighbor_coefficient_s_TeV2=K*LP**2*1e6/(8*HC**2),
    Planck_delay_4_vs_0point25TeV_s=K*LP**2*(4000**2-250**2)/(8*HC**2),
    length_bound_relative_to_LHAASO=6.9e11/scale,
    caveat='Published uncertainties and assumptions retained; arbitrary intrinsic source lags are not excluded')

runs=[]
for p in sorted(ROOT.rglob('*obs_id*.fits.gz')):
    with fits.open(p) as h:
        hd=h['EVENTS'].header
        if hd.get('OBJECT')!='PKS 2155-304' or not hd['DATE-OBS'].startswith('2006'):continue
        d=h['EVENTS'].data
        events=SkyCoord(d['RA']*u.deg,d['DEC']*u.deg)
        src=SkyCoord(hd['RA_OBJ']*u.deg,hd['DEC_OBJ']*u.deg)
        pnt=SkyCoord(hd['RA_PNT']*u.deg,hd['DEC_PNT']*u.deg)
        on_sep=events.separation(src).deg
        # Five reflected equal-area OFF apertures, for a background-count diagnostic.
        off_sep=np.array([events.separation(pnt.directional_offset_by(
            pnt.position_angle(src)+a*u.deg,pnt.separation(src))).deg for a in [60,120,180,240,300]])
        good=np.zeros(len(d),dtype=bool)
        for a,b in zip(h['GTI'].data['START'],h['GTI'].data['STOP']):
            good|=(d['TIME']>=a)&(d['TIME']<=b)
        runs.append(dict(obs_id=int(hd['OBS_ID']),date=hd['DATE-OBS'],
            start=float(hd['TSTART']),stop=float(hd['TSTOP']),
            safe_threshold_TeV=float(h['AEFF'].header['LO_THRES']),
            time=np.array(d['TIME'],float),energy=np.array(d['ENERGY'],float),
            sep=on_sep,off_sep=off_sep,good=good))
assert len(runs)==15
assert all(r['date']!='2006-07-28' for r in runs)
threshold=max(r['safe_threshold_TeV'] for r in runs)

def diagnostic(radius,iterations,seed):
    rng=np.random.default_rng(seed)
    terms=[];row=[]
    for r in runs:
        energycut=r['good']&(r['energy']>=threshold)&(r['energy']<=4)
        select=energycut&(r['sep']<radius)
        t=r['time'][select];e=r['energy'][select];n=len(t)
        off=int(sum(np.count_nonzero(energycut&(s<radius)) for s in r['off_sep']))
        row.append(dict(obs_id=r['obs_id'],date=r['date'],on_count=n,off_count=off,
            off_to_on_scale=.2,safe_threshold_TeV=r['safe_threshold_TeV'],
            tstart_s=r['start'],tstop_s=r['stop']))
        if n<3:continue
        # Scale ranks to common units, remove run intercepts, retain run sample sizes.
        x=(rankdata(t)-(n+1)/2)/n
        y=(rankdata(e)-(n+1)/2)/n
        terms.append((x,y))
    denom=np.sqrt(sum(x@x for x,y in terms)*sum(y@y for x,y in terms))
    observed=sum(x@y for x,y in terms)/denom
    null=np.zeros(iterations)
    for i in range(iterations):
        null[i]=sum(x@rng.permutation(y) for x,y in terms)/denom
    p=(1+np.count_nonzero(abs(null)>=abs(observed)))/(iterations+1)
    return dict(radius_deg=radius,energy_min_TeV=threshold,energy_max_TeV=4.,
        within_run_rank_association=float(observed),permutation_p_two_sided=float(p),
        permutation_count=iterations,seed=seed,on_count=sum(r['on_count'] for r in row),
        off_count=sum(r['off_count'] for r in row),
        estimated_background_on=sum(r['off_count'] for r in row)*.2,
        runs=row),null

primary,null=diagnostic(.11,5000,2155304)
sensitivity=[diagnostic(rad,2000,2155304)[0] for rad in [.08,.14]]
result=dict(analysis_date='2026-11-13',published_July28_result=published,
    public_data_use='Private technical demonstration only; DR1 terms prohibit scientific publications and new source claims',
    public_July29_30_diagnostic=primary,aperture_sensitivity=sensitivity,
    method='Within-run centered rank correlation between arrival time and reconstructed energy; shuffle energy labels within each run',
    data_are_original_published_LIV_sample=False,
    propagation_delay_fitted_to_public_data=False,
    limitations=['Public runs are a later flare and use different event reconstruction from the 2011 analysis',
        'Permutation null assumes energy and time independent within runs; detector changes and source evolution can violate it',
        'Run stratification removes between-run energy/acceptance differences, not within-run response changes',
        'Safe energy threshold is common to all runs; finite resolution and effective area are not forward folded',
        'Background is estimated with reflected apertures; event ranks are not background subtracted',
        'Association statistic is neither a calibrated lag estimate nor a propagation-only test',
        'A non-detection of rank association does not exclude an E-squared lag; this statistic has limited power',
        'Aperture checks are sensitivity diagnostics, not independent replications',
        'No new confidence bound or joint cross-source confidence interval is inferred'])
(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
np.savetxt(OUT/'run_counts.csv',np.array([[r['obs_id'],r['on_count'],r['off_count'],r['safe_threshold_TeV']] for r in primary['runs']]),
    delimiter=',',header='obs_id,on_count,off_count,safe_threshold_TeV',comments='')
np.save(OUT/'permutation_null.npy',null)
fig,ax=plt.subplots(figsize=(7.4,4.5))
ax.hist(null,bins=45,density=True,color='steelblue',alpha=.75,label='Energy-label permutations within runs')
ax.axvline(primary['within_run_rank_association'],color='darkred',lw=2,label='Observed association')
ax.set(xlabel='Within-run energy-time rank association',ylabel='Probability density',
       title=f'HESS DL3 DR1 technical demonstration: p = {primary["permutation_p_two_sided"]:.3f}')
ax.legend(fontsize=8)
fig.text(.5,.01,'HESS DL3 DR1, H.E.S.S. collaboration. Tool check only; no new scientific claim. See release terms.',ha='center',fontsize=7)
fig.tight_layout(rect=(0,.04,1,1));fig.savefig(OUT/'association_check.png',dpi=180);fig.savefig(OUT/'association_check.pdf')
manifest=dict(archive_url='https://www.mpi-hd.mpg.de/hfm/HESS/pages/dl3-dr1/hess_dl3_dr1.tar',
    terms_of_use_file='dl3/README.txt',
    archive_bytes=(OUT/'hess_dl3_dr1.tar').stat().st_size,
    archive_sha256=hashlib.sha256((OUT/'hess_dl3_dr1.tar').read_bytes()).hexdigest(),
    paper_sha256=hashlib.sha256((OUT/'paper.html').read_bytes()).hexdigest(),
    release_notes='https://www.mpi-hd.mpg.de/hfm/HESS/pages/dl3-dr1/hess_dl3_dr1.pdf',
    original_published_July28_event_data_located=False)
(OUT/'source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(published=published,primary={k:v for k,v in primary.items() if k!='runs'},
    sensitivity=[{k:v for k,v in x.items() if k!='runs'} for x in sensitivity]),indent=2))
