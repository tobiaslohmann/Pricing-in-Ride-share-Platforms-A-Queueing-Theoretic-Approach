import numpy as np
import pandas as pd
import Model_Queue
import agentSimulation


def main(mu_0, q_exit, bigLambda, gamma, tau, shape, theta, n, m, p_max):
    ### Pre-processing ###
    # Create df for solution
    column_names = ["Driver arrival paper", "Price", "Revenue paper", "Total time system running",
                    "Driver arrival agent based", "Revenue agent based total", "Revenue agent based per ride"]
    df_result = pd.DataFrame(columns=column_names)
    # Lists for Averages
    leng = [None] * m
    # Run-time simulation
    time = [None] * m
    rev = [None] * m
    ### Estimating balance price and demand optimal price ###
    pBal = Model_Queue.balancePriceStaticLarge(mu_0, gamma, tau, q_exit,
                                               bigLambda, shape)
    pd_opt = Model_Queue.demandOptimalPrice(shape)
    if pBal >= pd_opt:
        price = pBal
    else:
        price = pd_opt
    # Given from the paper
    plow = price * 0.75

    ### Simulation ###
    for i in np.arange(0.1, p_max, 0.1):
        # Pre-processing
        passengerArrival = Model_Queue.mu(i, mu_0, shape)
        driverArrival = Model_Queue.dynamicLam(plow, i, pBal, mu_0, q_exit, tau, gamma, bigLambda, shape)
        ### Building Averages ###
        # Run simulation m times for each price
        for j in np.arange(0, m):
            # Simulation
            df = agentSimulation.simulationDynamic(agentSimulation.create_df(n, passengerArrival),
                                                   agentSimulation.create_df(n, driverArrival), n,
                                                   driverArrival, passengerArrival, i, pBal, plow, gamma, theta, mu_0,
                                                   q_exit, tau, bigLambda,shape)
            ### Calculations ###
            df["RevenueCumSum"] = np.cumsum(df["Revenue"])
            leng[j] = len(df)
            rev[j] = max(df['RevenueCumSum'])
            time[j] = max(df['available_time_driver'])
            # Delete rows with all 0 - needed for Time Analysis only
            df = df.loc[~(df == 0).all(axis=1)]
            df.drop(df.tail(1).index, inplace=True)

        # Post-processing
        # Averagaes
        length = sum(leng) / len(leng)
        time_fin = sum(time) / len(time)
        Revenue = sum(rev)/len(rev)
        df_result.loc[i, "Driver arrival paper"] = driverArrival
        df_result.loc[i, "Price"] = i
        df_result.loc[i, "Revenue paper"] = Model_Queue.dynamicRevenue(plow, i, pBal, mu_0, q_exit, tau, bigLambda,
                                                                       shape, gamma, theta)
        df_result.loc[i, "Driver arrival agent based"] = length / time_fin
        df_result.loc[i, "Total time system running"] = time_fin
        df_result.loc[i, "Revenue agent based per ride"] = Revenue/time_fin
        # df_result.loc[i, "Revenue agent based per ride"] = df_result.loc[
        #                                                        i, "Driver arrival agent based"] * \
        #                                                    Model_Queue.dynamicMultiplier(plow, i, pBal, df_result.loc[
        #                                                        i, "Driver arrival agent based"], mu_0, shape, gamma,
        #                                                                                  theta)

    ### PLOT ###
    Model_Queue.plotAgentDynLam(df_result, p_max)
    Model_Queue.plotAgentDynRev(df_result, p_max)


    df.to_excel("/Users/laurinkrusselberg/Documents/dynTyry.xlsx")
