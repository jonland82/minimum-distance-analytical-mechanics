"""Prepare the companion note from saved results, without rerunning inference."""
from pathlib import Path
import json
import hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FILES = ['analysis/translated_bounds.json', 'analysis/ccf_results.json',
         'analysis/crab/results.json', 'analysis/pks2155/results.json']
loaded = [json.loads((ROOT / name).read_text()) for name in FILES]
grb, ccf, crab, pks = loaded
g = grb['translated_published_results'][1]
c = crab['translated_published_bounds'][-1]
p = pks['published_July28_result']
rows = [
    ('LHAASO: GRB 221009A', g['published_EQG2_lower_GeV'], g['Lambda_upper_m_from_rounded_EQG']),
    ('MAGIC: Crab pulsar', c['EQG2_lower_GeV'], c['Lambda_upper_m']),
    ('H.E.S.S.: PKS 2155--304', p['confidence95_EQG2_lower_GeV'], p['Lambda_upper_m']),
]
hc = grb['constants']['hbar_c_GeV_m']
lp = grb['constants']['Planck_length_m']
for _, scale, length in rows:
    assert np.isclose(scale * length, np.sqrt(12) * hc, rtol=1e-12, atol=0)

def texnum(x, digits=3):
    exponent = int(np.floor(np.log10(abs(x))))
    return rf'{x / 10.**exponent:.{digits-1}f}\times10^{{{exponent}}}'

table = [r'\begin{tabular}{lcc}', r'\hline',
         r'Observation & Published $E_{\mathrm{QG},2}$ lower limit & Translated $\Lambda$ upper limit \\',
         r' & (GeV) & (m) \\ \hline']
for label, scale, length in rows:
    table.append(rf'{label} & ${texnum(scale)}$ & ${texnum(length)}$ \\')
table += [r'\hline', r'\end{tabular}']
(HERE / 'results_table.tex').write_text('\n'.join(table) + '\n')

length_ratio = rows[0][2] / lp
values = dict(
    GRBUpper=rows[0][2], CrabUpper=rows[1][2], PKSUpper=rows[2][2],
    PlanckLength=lp, LengthGap=length_ratio, CoefficientGap=length_ratio**2,
    CountFactor=length_ratio**4,
    GRBPlanckDelay=grb['Planck_nearest_neighbor']['delay_7TeV_vs_0point2_s'],
    CrabPlanckDelay=crab['peak_comparisons'][1]['Planck_nearest_neighbor_delay_s'],
    PKSPlanckDelay=p['Planck_delay_4_vs_0point25TeV_s'],
    GRBHighestLag=ccf['lags_s'][-1], GRBHighestError=ccf['bootstrap_std_s'][-1],
)
commands = [rf'\newcommand{{\{name}}}{{{texnum(value)}}}' for name, value in values.items()]
(HERE / 'numbers.tex').write_text('\n'.join(commands) + '\n')

figdir = HERE / 'figures'
figdir.mkdir(exist_ok=True)
fig, ax = plt.subplots(figsize=(7.2, 2.5))
for i, (_, scale, length) in enumerate(rows):
    ax.annotate('', xy=(length / 15, i), xytext=(length, i),
                arrowprops=dict(arrowstyle='->', color='steelblue', lw=1.8))
    ax.scatter([length], [i], marker='|', s=180, color='steelblue')
    ax.text(length * 1.5, i, f'{length:.2e} m', va='center', fontsize=9)
ax.axvline(lp, color='black', ls='--', label='Planck length')
ax.set_xscale('log')
ax.set(xlim=(1e-36, 1e-24), ylim=(-.6, 2.6),
       xlabel='Effective interaction length $\\Lambda$ (m)',
       yticks=np.arange(3), yticklabels=['LHAASO / GRB', 'MAGIC / Crab', 'H.E.S.S. / PKS'])
ax.invert_yaxis()
ax.grid(axis='x', alpha=.25)
ax.legend(loc='lower left', fontsize=8)
fig.tight_layout()
fig.savefig(figdir / 'length_bounds.pdf')
fig.savefig(figdir / 'length_bounds.png', dpi=200)

manifest = dict(
    description='Companion note numerical inputs; no new confidence inference',
    generated_values=values,
    inputs=[dict(path=name, sha256=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()) for name in FILES],
    published_bounds=[dict(observation=name, EQG2_lower_GeV=e, Lambda_upper_m=l) for name,e,l in rows],
    excluded_from_scientific_results='HESS DL3 DR1 tool-only event diagnostic; no restricted archive outcomes or figures reproduced',
)
(HERE / 'provenance.json').write_text(json.dumps(manifest, indent=2))
print('Prepared table, numerical macros, figure and provenance from four saved result files.')
