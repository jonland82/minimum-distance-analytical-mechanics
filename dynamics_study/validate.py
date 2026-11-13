"""Independent checks of matrix spectra, derivatives and low-frequency order."""
from pathlib import Path
import json
import numpy as np
import mpmath as mp
from math import factorial
from study import central_a,central_b,b_to_a,speeds

OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'results.json').read_text())
checks=[]
N=129
for R in [1,2,4,8,16]:
    a=np.array(list(map(float,central_a(R))))
    matrix=np.eye(N)*2*a.sum()
    for r,v in enumerate(a,1):
        matrix-=v*(np.roll(np.eye(N),r,axis=1)+np.roll(np.eye(N),-r,axis=1))
    eigen=np.linalg.eigvalsh(matrix)
    x=2*np.pi*np.arange(N)/N
    prediction=speeds(central_b(R),x)[0]
    mismatch=float(np.max(abs(eigen-np.sort(prediction))))
    assert eigen.min()>-1e-12 and mismatch<1e-11
    xx=np.linspace(0,np.pi,10001)
    group=speeds(central_b(R),xx)[2]
    assert group.min()>-1e-13 and group.max()<1+1e-12
    assert abs(group[-1])<1e-12
    checks.append(dict(test='periodic_matrix_spectrum',range=R,max_mismatch=mismatch,
                       smallest_eigenvalue=float(eigen.min())))

for row in data['models']:
    if row['cap_over_pi']!=.5 or row['range']>6:continue
    a=b_to_a(row['b']);r=np.arange(1,len(a)+1)
    def freq(x):return np.sqrt(4*np.dot(a,np.sin(r*x/2)**2))
    points=np.array([.17,.73,1.5,2.9])
    step=1e-5
    numerical=np.array([(freq(x+step)-freq(x-step))/(2*step) for x in points])
    analytic=speeds(row['b'],points)[2]
    assert max(abs(numerical-analytic))<1e-7
    checks.append(dict(test='finite_difference_of_independent_cosine_symbol',
        range=row['range'],family=row['family'],max_mismatch=float(max(abs(numerical-analytic)))))

with mp.workdps(80):
    for R in [1,2,4,8]:
        x=mp.mpf('.01');y=mp.sin(x/2)**2
        b=[mp.mpf(v.numerator)/v.denominator for v in central_b(R)]
        D=sum(v*y**m for m,v in enumerate(b,1))
        derivative=sum(m*v*y**(m-1) for m,v in enumerate(b,1))
        vg=mp.sin(x)*derivative/(4*mp.sqrt(D))
        C=mp.mpf(2)*factorial(R)**2/factorial(2*R+2)
        expected=(2*R+1)*C/2
        ratio=(1-vg)/x**(2*R)/expected
        assert abs(ratio-1)<mp.mpf('.002')
        checks.append(dict(test='leading_group_error_coefficient',range=R,
                           measured_to_predicted_ratio=str(ratio)))

result=dict(all_passed=True,checks=checks,
    note='Complementary mathematical/numerical checks; no physical validation inferred')
(OUT/'verification.json').write_text(json.dumps(result,indent=2))
print('Passed',len(checks),'matrix-spectrum, numerical-derivative and asymptotic-coefficient checks.')
