
import numpy as np
import matplotlib.pyplot as plt
from utility_model import UM


""" Examples """
# Make networks
U_R = UM(m=1, coef_k1=0, coef_k2=0, seed=5) # U_R: Preferece ~ radom
U_R. add_nodes(N=100000)
U_D = UM(m=1, coef_k1=1, coef_k2=0, seed=5) # U_D: Preferece ~ k1
U_D. add_nodes(N=100000)
U_I = UM(m=1, coef_k1=0, coef_k2=1, seed=5) # U_I: Preferece ~ k2
U_I. add_nodes(N=100000)

# Calculate K2_bar (= K2_sum(t) / K1_sum(t)
k2_bar_U_R = np.array(U_R.K2_sum) / np.array(U_R.K1_sum)
k2_bar_U_D = np.array(U_D.K2_sum) / np.array(U_D.K1_sum)
k2_bar_U_I = np.array(U_I.K2_sum) / np.array(U_I.K1_sum)

# Plot K2_bar (Fig. 2 in Paper)
fig = plt.figure()
plt.plot(k2_bar_U_R, label='L0')
plt.plot(k2_bar_U_D, label='L1')
plt.plot(k2_bar_U_I, label='L2')
plt.legend()
plt.xscale('log')
plt.xlabel('t')
plt.ylabel(r'$\overline{k^{[2]}}$')
plt.show()