"""Stable lattice waves versus continuum propagation.

All experiments use dimensionless x=qk and a_r=g_r k^2/c^2.
These are mathematical/numerical model comparisons, not measured data.
"""
from pathlib import Path
from fractions import Fraction
from math import factorial, comb
import json, csv
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import linprog, minimize_scalar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent
(OUT/'figures').mkdir(exist_ok=True)

def central_a(R):
    return [Fraction(2*(-1)**(r+1)*factorial(R)**2,
                     r*r*factorial(R-r)*factorial(R+r)) for r in range(1,R+1)]

def central_b(R):
    return [Fraction(2*4**m,m*m*comb(2*m,m)) for m in range(1,R+1)]

def b_to_a(b):
    R=len(b)
    return np.array([sum((-1)**(r+1)*b[m-1]*comb(2*m,m-r)/4**m
                         for m in range(r,R+1)) for r in range(1,R+1)])

def speeds(b,x):
    """Stable polynomial evaluation avoids cancellations in signed stencils."""
    x=np.asarray(x,dtype=float)
    y=np.sin(x/2)**2
    # D=4y Q(y), where Q(0)=1.
    h=np.asarray(b,dtype=float)/4
    Q=np.polynomial.polynomial.polyval(y,h)
    deriv=np.polynomial.polynomial.polyval(y,np.arange(1,len(h))*h[1:]) if len(h)>1 else np.zeros_like(y)
    phase=np.sinc(x/(2*np.pi))*np.sqrt(Q)
    group=np.cos(x/2)*(Q+y*deriv)/np.sqrt(Q)
    symbol=4*y*Q
    return symbol,phase,group

def optimize_positive(R,cap):
    x=np.linspace(1e-6,cap,2001)
    rr=np.arange(1,R+1)
    A=(np.sinc(np.outer(x,rr)/(2*np.pi)))**2
    # w_r=a_r*r^2 are nonnegative and sum to one.
    C=np.vstack([np.column_stack([A,-np.ones(len(x))]),
                 np.column_stack([-A,-np.ones(len(x))])])
    res=linprog(np.r_[np.zeros(R),1.],A_ub=C,b_ub=np.r_[np.ones(len(x)),-np.ones(len(x))],
        A_eq=np.array([np.r_[np.ones(R),0.]]),b_eq=[1],bounds=[(0,None)]*(R+1),method='highs')
    if not res.success:raise RuntimeError(res.message)
    return dict(range=R,cap_over_pi=cap/np.pi,weights=res.x[:-1].tolist(),
                grid_squared_phase_error=float(res.x[-1]),
                analytic_error=float(1-np.sinc(cap/(2*np.pi))**2))

def optimize_stable(R,cap):
    """Minimax squared-phase error in a stability-certified subclass.

    D=4y[1+sum v_j (y/ymax)^j], v_j>=0. This includes the centered family,
    but does not exhaust globally stable signed stencils. LP is sampled.
    """
    if R==1:return [4.],dict(grid_objective=float(1-np.sinc(cap/(2*np.pi))**2),iterations=0)
    ymax=np.sin(cap/2)**2
    grid=np.linspace(1e-6,cap,1001)
    for iteration in range(6):
        y=np.sin(grid/2)**2
        baseline=np.sinc(grid/(2*np.pi))**2
        A=baseline[:,None]*(y[:,None]/ymax)**np.arange(1,R)
        C=np.vstack([np.column_stack([A,-np.ones(len(grid))]),
                     np.column_stack([-A,-np.ones(len(grid))])])
        rhs=np.r_[1-baseline,baseline-1]
        res=linprog(np.r_[np.zeros(R-1),1.],A_ub=C,b_ub=rhs,
            bounds=[(0,None)]*R,method='highs',options={
                'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10})
        if not res.success:raise RuntimeError(res.message)
        b=np.r_[4.,4*res.x[:-1]/ymax**np.arange(1,R)]
        dense=np.linspace(0,cap,20001)
        err=speeds(b,dense)[1]**2-1
        peaks=np.flatnonzero((abs(err[1:-1])>=abs(err[:-2]))&(abs(err[1:-1])>=abs(err[2:])))+1
        candidates=[cap]
        for j in peaks:
            opt=minimize_scalar(lambda z:-abs(speeds(b,np.array([z]))[1][0]**2-1),
                bounds=(dense[j-1],dense[j+1]),method='bounded',options={'xatol':1e-13})
            candidates.append(float(opt.x))
        errors=[abs(speeds(b,np.array([z]))[1][0]**2-1) for z in candidates]
        if max(errors)<=res.x[-1]+2e-10:break
        grid=np.unique(np.r_[grid,candidates])
    return b.tolist(),dict(grid_objective=float(res.x[-1]),iterations=iteration+1,
                          refined_max_squared_phase_error=float(max(errors)),
                          LP_feasibility_tolerance=1e-10,
                          scope='sampled minimax in positive-y-polynomial subclass; not all stable signed stencils')

def metrics(b,cap):
    x=np.linspace(0,cap,100001)
    D,vp,vg=speeds(b,x)
    whole=np.linspace(0,np.pi,100001)
    Dw,pw,gw=speeds(b,whole)
    return dict(max_squared_phase_error=float(np.max(abs(vp**2-1))),
        max_phase_speed_error=float(np.max(abs(vp-1))),
        max_group_speed_error=float(np.max(abs(vg-1))),
        min_group_speed_in_band=float(vg.min()),max_group_speed_in_band=float(vg.max()),
        min_D_over_x2_full_zone=float(np.min(pw**2)),
        max_group_speed_full_zone=float(gw.max()),
        band_samples=len(x),full_zone_samples=len(whole))

def verify_exact():
    y=sp.Symbol('y')
    results=[]
    for R in [1,2,3,4,6,8,12,16]:
        a=central_a(R);b=central_b(R)
        assert sum(a[r-1]*r*r for r in range(1,R+1))==1
        for m in range(2,R+1):assert sum(a[r-1]*r**(2*m) for r in range(1,R+1))==0
        symbol=sum(2*sp.Rational(z.numerator,z.denominator)*(1-sp.chebyshevt(r,1-2*y))
                   for r,z in enumerate(a,1))
        polynomial=sum(sp.Rational(z.numerator,z.denominator)*y**m for m,z in enumerate(b,1))
        assert sp.expand(symbol-polynomial)==0
        assert all(z>0 for z in b)
        # An exact polynomial certificate of vg^2 <= 1 on the full zone.
        gap=sp.Poly(sp.expand(4*polynomial-y*(1-y)*sp.diff(polynomial,y)**2),y)
        assert all(coeff>=0 for coeff in gap.all_coeffs())
        first=sum(a[r-1]*r**(2*R+2) for r in range(1,R+1))
        assert first!=0
        results.append(dict(range=R,normalization=True,cancelled_even_moments=list(range(4,2*R+1,2)),
            first_uncancelled_moment=str(first),symbol_equals_positive_polynomial=True,
            global_nonnegative_energy_certificate=True,global_group_speed_bound_certificate=True))
    return results

def main():
    exact=verify_exact()
    runs=[];positive=[]
    for cap_fraction in [.25,.5,.75]:
        cap=cap_fraction*np.pi
        for R in [1,2,3,4,6]:
            positive.append(optimize_positive(R,cap))
        for R in [1,2,3,4,6,8,12,16]:
            b=list(map(float,central_b(R)))
            with mp.workdps(70):
                xx=mp.mpf(str(cap_fraction))*mp.pi;yy=mp.sin(xx/2)**2
                bb=[mp.mpf(v.numerator)/v.denominator for v in central_b(R)]
                DD=sum(v*yy**m for m,v in enumerate(bb,1))
                DP=sum(m*v*yy**(m-1) for m,v in enumerate(bb,1))
                hp_phase=str(1-mp.sqrt(DD)/xx)
                hp_group=str(1-mp.sin(xx)*DP/(4*mp.sqrt(DD)))
            runs.append(dict(family='centered',range=R,cap_over_pi=cap_fraction,
                a=[str(v) for v in central_a(R)],b=b,
                leading_group_error_order=2*R,
                high_precision_endpoint_phase_error=hp_phase,
                high_precision_endpoint_group_error=hp_group,**metrics(b,cap)))
        for R in [2,3,4,6]:
            b,opt=optimize_stable(R,cap)
            runs.append(dict(family='band_optimized',range=R,cap_over_pi=cap_fraction,
                a=b_to_a(b).tolist(),b=b,optimization=opt,**metrics(b,cap)))
    # Verify numerical properties against the analytical statements.
    for pos in positive:
        assert abs(pos['grid_squared_phase_error']-pos['analytic_error'])<1e-7
    for row in runs:
        assert row['min_D_over_x2_full_zone']>0
        assert row['b'][0]==4 and all(x>=0 for x in row['b'])
        assert abs(np.dot(b_to_a(row['b']),np.arange(1,row['range']+1)**2)-1)<1e-8
    result=dict(dimensionless_conventions='x=qk, a_r=g_r*k^2/c^2, D=(omega*k/c)^2',
        data_origin='numerical models only; no physical experiment or minimum-distance evidence',
        exact_symbolic_checks=exact,positive_coupling_LP_checks=positive,models=runs,
        optimization_scope='finite-band squared-phase error in the subclass D=4y+sum b_m*y^m with b_m>=0',
        stability='exact polynomial positivity for centered rules; coefficient-sign certificate for optimized rules',
        limitations=['No physical mechanism selecting signed interactions is supplied',
                     'Numerical max errors are dense-grid estimates, not certified global extrema',
                     'Float64 errors near 1e-15 reach a numerical floor; 70-digit endpoint checks are stored separately',
                     'LP results are sampled/subclass optima with finite solver tolerances',
                     'Phase-error optimization does not optimize group velocity',
                     'Global spectral stability does not imply a strict causal front or relativistic invariance'])
    (OUT/'results.json').write_text(json.dumps(result,indent=2))
    columns=['family','range','cap_over_pi','max_squared_phase_error','max_phase_speed_error',
             'max_group_speed_error','max_group_speed_full_zone']
    with (OUT/'errors.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader()
        for row in runs:w.writerow({k:row[k] for k in columns})
    plot(runs)
    lines=[r'\begin{tabular}{llrr}',r'\hline',
        r'Family & Range $R$ & Max. phase error & Max. group error \\ \hline']
    for row in runs:
        if row['cap_over_pi']==.5 and row['range'] in [1,2,4,6]:
            name='Centered' if row['family']=='centered' else 'Band-optimized'
            lines.append(f"{name} & {row['range']} & ${row['max_phase_speed_error']:.2e}$ & ${row['max_group_speed_error']:.2e}$" + r' \\')
    lines += [r'\hline',r'\end{tabular}']
    # Scientific notation for portable LaTeX.
    import re
    table='\n'.join(lines)
    table=re.sub(r'([0-9.]+)e([+-])(\d+)',lambda m:m[1]+r'\times10^{'+('-' if m[2]=='-' else '')+str(int(m[3]))+'}',table)
    (OUT/'error_table.tex').write_text(table+'\n')
    for row in runs:
        if row['cap_over_pi']==.5:
            print(row['family'],row['range'],'phase',f"{row['max_phase_speed_error']:.5g}",
                'group',f"{row['max_group_speed_error']:.5g}",'max vg',f"{row['max_group_speed_full_zone']:.5g}")
    print('All exact identities and numerical consistency checks passed.')

def plot(rows):
    x=np.linspace(0,np.pi,2001)
    fig,axes=plt.subplots(1,2,figsize=(9,3.7))
    for R in [1,2,4,8,16]:
        D,vp,vg=speeds(central_b(R),x)
        axes[0].plot(x/np.pi,vp,label=f'R={R}')
        axes[1].plot(x/np.pi,vg,label=f'R={R}')
    for ax,ylabel in zip(axes,['Phase speed / c','Group speed / c']):
        ax.axhline(1,color='black',ls='--',lw=.8)
        ax.set(xlabel=r'$qk/\pi$',ylabel=ylabel);ax.grid(alpha=.2)
    axes[0].legend(fontsize=8);fig.tight_layout()
    fig.savefig(OUT/'figures/dispersion.pdf');fig.savefig(OUT/'figures/dispersion.png',dpi=180)
    fig,axes=plt.subplots(1,2,figsize=(9,3.7))
    for frac in [.25,.5,.75]:
        sel=[r for r in rows if r['family']=='centered' and r['cap_over_pi']==frac]
        axes[0].semilogy([r['range'] for r in sel],[max(r['max_phase_speed_error'],1e-16) for r in sel],
                         'o-',label=rf'$q_{{max}}k={frac}\pi$')
        axes[1].semilogy([r['range'] for r in sel],[max(r['max_group_speed_error'],1e-16) for r in sel],'o-')
    axes[0].set(ylabel='Maximum phase-speed error');axes[1].set(ylabel='Maximum group-speed error')
    for ax in axes:ax.set(xlabel='Interaction range R (lattice steps)');ax.grid(alpha=.2)
    axes[0].legend(fontsize=8);fig.tight_layout()
    fig.savefig(OUT/'figures/convergence.pdf');fig.savefig(OUT/'figures/convergence.png',dpi=180)
    fig,axes=plt.subplots(1,2,figsize=(9,3.7));x=np.linspace(0,np.pi/2,2001)
    for family,R in [('centered',1),('centered',4),('band_optimized',4)]:
        row=next(r for r in rows if r['family']==family and r['range']==R and r['cap_over_pi']==.5)
        D,vp,vg=speeds(row['b'],x)
        axes[0].plot(x/np.pi,vp-1,label=f'{family}, R={R}')
        axes[1].plot(x/np.pi,vg-1,label=f'{family}, R={R}')
    for ax,ylabel in zip(axes,['Phase speed / c - 1','Group speed / c - 1']):
        ax.set(xlabel=r'$qk/\pi$',ylabel=ylabel)
        ax.set_yscale('symlog',linthresh=1e-7);ax.grid(alpha=.2)
    axes[0].legend(fontsize=7);fig.tight_layout()
    fig.savefig(OUT/'figures/optimized.pdf');fig.savefig(OUT/'figures/optimized.png',dpi=180)

if __name__=='__main__':main()
