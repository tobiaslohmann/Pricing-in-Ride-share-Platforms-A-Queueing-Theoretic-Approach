import numpy as np
import static_theoretic
import dynamic_theoretic
import static_agent
import dynamic_agent
import pandas as pd

### INPUT ###
mu_0 = 4                        # Potential ride request
lambda_0 = 1                    # Potential new drivers
q_exit = .5                     # Probability driver leaving the system
gamma = 0.0000001               # Fraction the drivers earn | gamma = 0 for max. platform revenue
tau = 0.0000001                 # Exponential service time
theta_0 = 3                     # Threshold | Dynamic pricing
n = 10000000000000000000        # To simulate the large market limit n --> infinty
theta = theta_0 * np.log(n)     # Threshold in the nth system
shape = 2                       # Shape GAMMA distribution
### Simulation ###
p_max = 5.1                     # Upper price limit for simulation
n = 3300                        # Static Pricing | Simulating n matches of passengers and drivers in the system
m = 2                           # Building the average of m occurrences for every price p
time = 5000                   # Dynamic Pricing | Time simulation of dynamic pricing

if __name__ == '__main__':
    ### Static | Large market limit | Theoretic
    static_theoretic.main(mu_0, q_exit, lambda_0, gamma, tau, shape)
    ### Static | Large market limit | Agent
    static_agent.main(mu_0, q_exit, lambda_0, gamma, tau, shape, n, m, p_max)
    # Dynamic | Large market limit | Theoretic
    dynamic_theoretic.main(mu_0, q_exit, lambda_0, gamma, tau, shape, theta)
    ### Dynamic | Large market limit | Agent                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             namic | Large market limit | Agent
    dynamic_agent.main(mu_0, q_exit, lambda_0, gamma, tau, shape, theta, m, p_max, time)
