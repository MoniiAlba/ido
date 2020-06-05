import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

mpl.style.use('seaborn')


T = 80 # Simulation time
kids = np.zeros(T)
adults = np.zeros(T)
mature = np.zeros(T)

# State T = 0
kids[0] = 100
adults[0] = 800
mature[0] = 100

# Rates
reproduce = (3.1/20) /2
die = 0.03
to_adult = 1/21
to_mature = 1/20

for t in range (1, T):
    k = kids[t-1]
    a = adults[t-1]
    m = mature[t-1]

    kids[t] = k - k * to_adult + a * reproduce
    adults[t] = a - a * to_mature + k * to_adult
    mature[t] = m - m*die + a * to_mature

plt.plot(np.arange(0,T), kids, label='Kids')
plt.plot(np.arange(0,T), adults, label='Adults')
plt.plot(np.arange(0,T), mature, label='Mature')
plt.legend(loc='center right')
plt.show()
