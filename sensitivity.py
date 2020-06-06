from scipy.integrate import solve_ivp
from scipy.stats import pearsonr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

mpl.style.use('seaborn')

#-------------- SEIR POBLACIONAL -----------------------

#------ Variables iniciales ----------
# En SEIR agregamos stock de latentes (E) y muertos
# N -> total poblacion
# I0 -> infectados iniciales
# S0 -> susceptibles iniciales
# R0 -> recuperados iniciales
# E0 -> latentes iniciales

N =  100_000

I0 = 0
S0 = N - I0
E0 = 1
R0 = 0
M0 = 0

Y0 = (S0, E0, I0, R0, M0)

#CE = 1.5
fraccion_muertos = 0.116    #dato obtenido de la tasa de mortalidad del covid-19
#tiempo_recuperacion = 3     #duracion de la infeccion
f = 14

def seirs_model(t, y, CE, D, N):
    susceptibles, latentes, infectados, recuperados, muertos = y

    β = CE / N
    λ = β * infectados

    # Flujos
    ER = susceptibles * λ                   #flujo latentes
    IR =  latentes / f                      #flujo infectados
    MR = infectados * fraccion_muertos      #flujo muertos
    RR = infectados / D   #flujo recuperados

    # Stocks
    ds = - ER
    de = ER - IR
    di = IR - RR - MR
    dm = MR
    dr = RR

    return (ds, de, di, dr, dm)

# ======================= ANALISIS DE SENSIBILIDAD =================================

rangos = {
    'CE': (0,7),
    'D': (1,10),
    'I0': (1,25),
    'E0': (0,25)
}

def latin_hypercube_uniform(ranges, samples):
    parameter_names = ranges.keys()
    minimos = np.array([value[0] for key,value in ranges.items()])
    maximos = np.array([value[1] for key,value in ranges.items()])
    lower_limits, step = np.linspace(minimos, maximos, samples, endpoint=False, retstep=True)
    upper_limits = lower_limits + step

    points = np.random.default_rng().uniform(lower_limits, high=upper_limits).T

    for i in np.arange(1, len(parameter_names)):
        np.random.shuffle(points[i])

    return (points, parameter_names)


def run_sims(parameters, ts):
    corridas = []
    for param in parameters.T:
        CE, D, I0, E0 = param
        N = 100_000
        S0, R0, M0 = N - I0 - E0, 0, 0
        Y0 = (S0, E0, I0, R0, M0)

        sol = solve_ivp(seirs_model, [0,ts], Y0, args = (CE, D, N), t_eval=np.arange(0,ts,0.125))

        corridas.append(sol.y)

    corridas = np.dstack(corridas)

    return corridas

ts = 150
n_muestras = 300
parameters, _ = latin_hypercube_uniform(rangos, n_muestras)
corridas = run_sims(parameters, ts)
corridas.shape

plt.plot(np.arange(0, ts, 0.125), corridas[1,:,:], c='b', alpha = 0.05)
plt.ylim([0,100_000])
plt.xlim([0,ts])
plt.title('HOLI')
plt.show()


y = corridas[1,:,:]
n=1

perc1 = np.percentile(y, np.linspace(1, 50, num=n, endpoint=False), axis=1)
perc2 = np.percentile(y, np.linspace(50, 99, num=n+1)[1:], axis=1)

for p1, p2 in zip(perc1, perc2):
    plt.fill_between(np.arange(0,ts,0.125), p1,p2, alpha=1, color='lightgrey', edgecolor=None, label="99%")



perc1 = np.percentile(y, np.linspace(5, 50, num=n, endpoint=False), axis=1)
perc2 = np.percentile(y, np.linspace(50, 95, num=n+1)[1:], axis=1)

for p1, p2 in zip(perc1, perc2):
    plt.fill_between(np.arange(0,ts,0.125), p1,p2, alpha=1, color='silver', edgecolor=None, label="90%")


perc1 = np.percentile(y, np.linspace(25, 50, num=n, endpoint=False), axis=1)
perc2 = np.percentile(y, np.linspace(50, 75, num=n+1)[1:], axis=1)

for p1, p2 in zip(perc1, perc2):
    plt.fill_between(np.arange(0,ts,0.125), p1,p2, alpha=0.5, color='dimgrey', edgecolor=None, label="50%")

plt.plot(np.arange(0,ts,0.125), np.mean(y, axis=1), color='k', linestyle=":", label='mean')
plt.plot(np.arange(0,ts,0.125), np.median(y, axis=1), color='k', label="median")
plt.legend()

plt.ylim([0,100_000])
plt.xlim([0,ts])

plt.show()


# ======================= STATISTICAL SCREENING =================================



infecciosos = corridas[1,:,:] # Shape t x simulaciones
CEs = parameters[0] # shape simulaciones
Ds = parameters[1]
I0s = parameters[2]
E0s = parameters[3]

corr_CE = np.apply_along_axis(pearsonr,1,infecciosos, CEs)[:,0] # Descartamos p-value
corr_D =  np.apply_along_axis(pearsonr,1,infecciosos, Ds)[:,0]
corr_I0 =  np.apply_along_axis(pearsonr,1,infecciosos, I0s)[:,0]
corr_E0 =  np.apply_along_axis(pearsonr,1,infecciosos, E0s)[:,0]

infecciosos_promedio = np.mean(infecciosos, axis=1)

simulation_time = np.arange(0,ts,0.125)
fig, axes = plt.subplots(2,1, sharex=True)

axes[0].set_xlim(0,20)
axes[0].plot(simulation_time, infecciosos_promedio, 'k')
axes[1].plot(simulation_time, corr_CE, 'g', label='CE')
axes[1].plot(simulation_time, corr_D, 'b', label='D')
axes[1].plot(simulation_time, corr_I0, 'r', label='I0')
axes[1].plot(simulation_time, corr_E0, 'c', label='E0')
axes[1].legend()
axes[1].set_xlabel('Días')

fig.tight_layout()

np.argwhere(simulation_time == 17)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.boxplot([corr_CE[:136], corr_D[:136], corr_I0[:136], corr_E0[:136]])
ax.set_xticklabels(['CE', 'D', 'I0', 'E0'])
fig.tight_layout()

plt.show()
