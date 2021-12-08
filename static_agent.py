import numpy as np
import pandas as pd
import Model_Queue
import static_simulation


def main(mu_0, q_exit, lambda_0, gamma, tau, shape, n, m, p_max):
    ### Pre-processing ###
    # Create df for solution
    column_names = ["Price", "Simulation time", "Driver arrival rate | Agent", "Driver arrival rate | Theoretic",
                    "Revenue | Agent", "Revenue | Theoretic"]
    df_result = pd.DataFrame(columns=column_names)
    # Lists for Averages
    leng = [None] * m
    rev = [None] * m
    # Run-time simulation
    time = [None] * m
    ### Simulation ###
    for i in np.arange(0.1, p_max, 0.1):
        # Pre-processing
        p_arrival_rate = Model_Queue.mu(i, mu_0, shape)
        d_arrival_rate = Model_Queue.lambda_static(i, gamma, tau, mu_0, lambda_0, q_exit, shape)
        ### Building Averages ###
        # Run simulation m times for each price
        for j in np.arange(0, m):
            # Simulation
            df = static_simulation.simulation(static_simulation.create_df(n, p_arrival_rate),
                                              static_simulation.create_df(n, d_arrival_rate), n,
                                              d_arrival_rate, p_arrival_rate, i, gamma)
            ### Calculations ###
            df["RevenueCumSum"] = np.cumsum(df["Revenue"])
            leng[j] = len(df)
            rev[j] = max(df['RevenueCumSum'])
            time[j] = max(df['available_time_driver'])

        # Post-processing
        length = sum(leng) / len(leng)
        Revenue = sum(rev) / len(rev)
        time_fin = sum(time) / len(time)
        df_result.loc[i, "Price"] = i
        df_result.loc[i, "Simulation time"] = time_fin
        df_result.loc[i, "Driver arrival rate | Agent"] = length / time_fin
        df_result.loc[i, "Driver arrival rate | Theoretic"] = d_arrival_rate
        df_result.loc[i, "Revenue | Agent"] = Revenue / time_fin
        df_result.loc[i, "Revenue | Theoretic"] = i * d_arrival_rate * (1 - gamma)

    ### PLOT ###
    Model_Queue.plotStaticAgentLambda(df_result, p_max)
    Model_Queue.plotStaticAgentRevenue(df_result, p_max)
