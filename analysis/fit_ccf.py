"""Exploratory timing check from released WCDA light curves.

Uses a fixed, documented CCF peak estimator and joint Poisson bootstrap.
Median-energy regression is diagnostic only: it omits response/bias correction.
"""
import json
from pathlib import Path
import numpy as np
import uproot
from scipy.signal import correlate, correlation_lags
from scipy.optimize import curve_fit
from scipy.stats import chi2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent
f=uproot.open(next((OUT/'lhaaso_data').rglob('light_curve.root')))
t=f['h1d_on_nq03t30_0'].axis().centers()
mask=(t>=232)&(t<400)
on=np.array([f[f'h1d_on_nq03t30_{j}'].values()[mask] for j in range(10)])
off=np.array([f[f'h1d_bk_nq03t30_{j}'].values()[mask] for j in range(10)])
dt=.1
lags=correlation_lags(on.shape[1],on.shape[1])*dt
use=np.abs(lags)<=20
x=lags[use]

def gaussian(x, baseline, amp, center, width):
    return baseline+amp*np.exp(-.5*((x-center)/width)**2)

def measure(a,b,window=10):
    y=correlate(b,a,mode='full',method='fft')[use]
    y/=np.sqrt(np.dot(a,a)*np.dot(b,b))
    # Fit a symmetric fixed interval about zero to avoid selecting noise peaks.
    pick=np.abs(x)<=window
    p,_=curve_fit(gaussian,x[pick],y[pick],p0=[y[pick].min(),.2,0,10],
        bounds=([-2,0,-15,1],[2,4,15,80]),maxfev=3000)
    return p[2],y,p

def delays(signal,window=10):
    return np.array([measure(signal[0],signal[j],window)[0] for j in range(1,10)])

observed=delays(on-off)
rng=np.random.default_rng(221009)
samples=[]
for n in range(500):
    # Released OFF histograms are four times ON exposure, scaled by 1/4.
    mock_on=rng.poisson(on)
    mock_off=rng.poisson(off*4)/4
    samples.append(delays(mock_on-mock_off))
    if n%100==99:print('bootstrap',n+1,flush=True)
samples=np.array(samples)
cov=np.cov(samples,rowvar=False)
errors=np.sqrt(np.diag(cov))
ci=np.percentile(samples,[2.5,97.5],axis=0)

# Conventional median-energy regression; response overlap can strongly bias it.
medians=np.array([.354,.375,.395,.419,.457,.486,.556,.658,.843,1.601])
translation=json.loads((OUT/'translated_bounds.json').read_text())
K2=translation['constants']['K2_s'];ep=translation['constants']['Planck_energy_GeV']
design=1.5*K2*1e15/ep**2*1e6*(medians[1:]**2-medians[0]**2)
inv=np.linalg.inv(cov)
eta=float(design@inv@observed/(design@inv@design))
sigma=float(1/np.sqrt(design@inv@design))
null_chi=float(observed@inv@observed)
result=dict(
    status='Exploratory independent CCF check, not a reproduction of the response-corrected published fit',
    time_window_s=[232,400],time_bin_s=.1,bootstrap_replicates=len(samples),seed=221009,
    count_on=on.sum(axis=1).tolist(),count_background=off.sum(axis=1).tolist(),
    median_energies_TeV=medians.tolist(),lags_s=observed.tolist(),bootstrap_std_s=errors.tolist(),
    bootstrap_percentiles_s=ci.tolist(),covariance_s2=cov.tolist(),
    zero_lag_chi2=null_chi,zero_lag_dof=9,zero_lag_approx_p=float(chi2.sf(null_chi,9)),
    uncorrected_median_energy_eta2=eta,uncorrected_eta2_std=sigma,
    sensitivity_to_peak_fit_window={str(w):delays(on-off,w).tolist() for w in [8,10,15]},
    limitations=['Fixed Gaussian CCF peak estimator; differs from collaboration implementation',
                 'Poisson bootstrap at observed bin counts; approximate intervals',
                 'Channels share the same reference; bootstrap covariance is retained',
                 'Median-energy regression ignores broad response and spectral-evolution bias',
                 'No propagation-only confidence bound or detection claim can be assigned from this diagnostic',
                 'Intrinsic source lags remain unconstrained'],
)
(OUT/'ccf_results.json').write_text(json.dumps(result,indent=2))
np.savetxt(OUT/'measured_lags.csv',np.column_stack([np.arange(1,10),medians[1:],observed,errors]),
           delimiter=',',header='segment,median_energy_TeV,lag_s,bootstrap_std_s',comments='')
fig,ax=plt.subplots(figsize=(7,4.5))
ax.errorbar(medians[1:],observed,yerr=errors,fmt='o',label='Released counts; exploratory CCF (1 sigma)')
ax.axhline(0,color='k',lw=1,label='Zero delay')
ax.set(xlabel='Median channel energy (TeV)',ylabel='Lag relative to lowest channel (s)',
       title='GRB 221009A: independent timing diagnostic')
ax.legend(fontsize=8);ax.grid(alpha=.2)
fig.tight_layout();fig.savefig(OUT/'measured_lags.png',dpi=180)
fig.savefig(OUT/'measured_lags.pdf')
print(json.dumps({k:v for k,v in result.items() if k not in ['covariance_s2']},indent=2))
