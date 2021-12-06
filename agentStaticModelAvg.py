import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
import Model_Queue
import agentSimulation

def main(mu_0, q_exit, bigLambda, gamma, tau, shape, n, m, p_max):
    ### Pre-processing ###
    # Create df for solution
    column_names = ["Driver arrival paper", "Price", "Revenue paper", "Total time system running",
        "Driver arrival agent based", "Revenue agent based total", "Revenue agent based per ride"]
    df_result = pd.DataFrame(columns = column_names)
    # Lists for Averages
    leng = [None]*m
    rev = [None]*m
    # Run-time simulation
    time = [None]*m
    ### Simulation ###
    for i in np.arange(0.1, p_max, 0.1):
        # Pre-processing
        passengerArrival = Model_Queue.mu(i, mu_0, shape)
        driverArrival = Model_Queue.lamlarge(i, gamma, tau, mu_0,
                                             bigLambda, q_exit, shape)
        ### Building Averages ###
        # Run simulation m times for each price
        for j in np.arange(0,m):
            # Simulation
            df = agentSimulation.simulationStatic(agentSimulation.create_df(n, passengerArrival),
                                                agentSimulation.create_df(n, driverArrival), n,
                                                driverArrival, passengerArrival, i, gamma)
            ### Calculations ###
            df["RevenueCumSum"] = np.cumsum(df["Revenue"])
            leng[j] = len(df)
            rev[j] = max(df['RevenueCumSum'])
            time[j] = max(df['available_time_driver'])
            # Delete rows with all 0 - needed for Time Analysis only
            df = df.loc[~(df == 0).all(axis=1)]
            df.drop(df.tail(1).index, inplace=True)

        # Post-processing
        length = sum(leng)/len(leng)
        Revenue = sum(rev)/len(rev)
        time_fin = sum(time)/len(time)
        df_result.loc[i, "Driver arrival paper"] = driverArrival
        df_result.loc[i, "Price"] = i
        df_result.loc[i, "Revenue paper"] = i*driverArrival*(1-gamma)
        df_result.loc[i, "Driver arrival agent based"] = length / time_fin
        df_result.loc[i, "Total time system running"] = time_fin
        df_result.loc[i, "Revenue agent based total"] = Revenue
        df_result.loc[i, "Revenue agent based per ride"] = Revenue / time_fin

    ### PLOT ###
    Model_Queue.plotAgentLam(df_result, p_max)
    Model_Queue.plotAgentRev(df_result, p_max)