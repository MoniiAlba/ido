from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

mpl.style.use('seaborn')

N =  100_000
I0 = 1
S0 = N - I0
R0 = 0
Q0 = 0
Y0 = (S0, I0, R0, Q0)

CE = 2
D = 2

VF = 0.05
QF = 0.05

def sir_model_policy(t, y, CE, D, N, VF, QF):
    s,i,r,q = y

    β = CE / N
    λ = β * i


    VR = s * VF
    QR = i * QF
    QRR = q / D
    IR = s * λ
    RR = i / D


    ds = -(IR+VR)
    di = IR - (RR+QR)
    dr = RR + VR + QRR
    dq = QR - QRR
    return (ds, di, dr, dq)

ts = 50
sol = solve_ivp(sir_model_policy, [0,ts], Y0, args=(CE, D, N, VF, QF), t_eval=np.arange(0,ts,0.125))

plt.plot(sol.t, sol.y.T, label=['S' 'I', 'R', 'Q'])
plt.legend(['S','I','R', 'Q'],loc='upper right')
plt.show()
