import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

mpl.style.use('seaborn')


T = 15 # Tiempo de simulación

# Stocks
customers = np.zeros(T)

# Flujos
recruits = np.zeros(T)
losses = np.zeros(T)

# Estado en T = 0
customers[0] = 10_000

def step(amount, time, t):
    if t <= time :
	    return 0
    else:
	    return amount

for t in range(1, T):
    c = customers[t-1]

    # Auxiliares
    growth_fraction = 0.07 - step(0.04,5, t) - step(0.01, 10, t)
    decline_fraction = 0.03

    recruits[t] = c * growth_fraction
    losses[t] = c * decline_fraction

    customers[t] = c + recruits[t] - losses[t]

plt.plot(np.arange(0,T), recruits, label='Recruits')
plt.plot(np.arange(0,T), losses, label='Losses')
plt.plot(np.arange(0,T), customers, label='Customers')
plt.legend(loc='center right')
plt.show()

