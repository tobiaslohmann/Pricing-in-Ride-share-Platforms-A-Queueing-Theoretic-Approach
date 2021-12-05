import numpy as np
import theoreticStaticModel
import theoreticDynamicModel
import agentStaticModelAvg
import agentDynamicModel

### INPUT VARIABLES ###
# bigLambda/q_exit = 2
bigLambda = 1
q_exit = .5
mu_0 = 4
# Gamma/tau = 1
# Gamma --> 0 to plot the max revenue of the platform
gamma = 0.0000001
tau = 0.0000001

# Theta in the  large market limit: n goes to infinity
theta_0 = 3
n = 10000000000000000000
theta = theta_0 * np.log(n)

### GAMMA DISTRIBUTION ###
shape = 2

# Upper price limit for simulation
p_max = 5.1

### Simulating n matches of passengers and drivers in the system ###
n = 3300

### Building the average of m occurences for every price p
m = 10

if __name__ == '__main__':
    ### Static | Large market limit | Theoretic
    # theoreticStaticModel.main(mu_0, q_exit, bigLambda, gamma, tau, shape)
    ### Static | Large market limit | Agent
    # agentStaticModelAvg.main(mu_0, q_exit, bigLambda, gamma, tau, shape, n, m, p_max)
    # Dynnamic | Large market limit | Theoretic
    # theoreticDynamicModel.main(mu_0, q_exit, bigLambda, gamma, tau, shape, theta)
    ### Dynnamic | Large market limit | Agent
    agentDynamicModel.main(mu_0, q_exit, bigLambda, gamma, tau, shape, theta, n, m, p_max)
