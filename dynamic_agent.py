import numpy as np
import pandas as pd
import Model_Queue
import dynamic_simulation


def main(mu_0, q_exit, lambda_0, gamma, tau, shape, theta, m, p_max, time):
    p_bal = Model_Queue.balance_price(mu_0, gamma, tau, q_exit,
                                      lambda_0, shape)
    p_low = 0.75 * p_bal
    # Start of p_high
    p_high = 0
    print("Balnce Price: ", p_bal)
    s = dynamic_simulation.Simulation(p_high, p_low, p_bal, mu_0, q_exit, tau, gamma, lambda_0, shape)
    j = 0
    column_names = ["Price i", "Time", "Drivers arrived to system", "Driver arrival rate | Agent",
                    "Driver arrival rate | Theoretic", "Expected earnings per ride | Agent",
                    "Expected earnings per ride | Theoretic", "Revenue | Agent", "Revenue | Theoretic"]
    df_result = pd.DataFrame(columns=column_names)
    for i in np.arange(0.1, p_max, 0.1):
        p_high = i
        # if p_high and p_low arr smaller than p_bal --> higher price is set by platform
        if p_high < p_low:
            p_high = p_low
        for k in np.arange(0, m):
            # For simulation: Follow the state of the simulation
            print(i, " :  ", k)

            df = pd.DataFrame(
                columns=['Clock', 'passenger Arrival', 'driver Arrival', 'passenger queue', 'driver queue', 'start',
                         'end', 'price', 'driverArrival', 'passengerArrival'])
            s.__init__(p_high, p_low, p_bal, mu_0, q_exit, tau, gamma, lambda_0, shape)
            ### Simulation ###
            while s.clock <= time:
                s.time()
                df = df.append(pd.Series(
                    [s.clock, s.p_arrival, s.d_arrival, s.queue_p, s.queue_d, s.start, s.end, s.price, s.driverArrival,
                     s.passengerArrival],
                    index=df.columns), ignore_index=True)
                # Single threshold
                if s.queue_d > theta:
                    s.price = p_low
                    s.driverArrival = Model_Queue.lambda_gamma(s.price, s.gamma, s.tau, s.lambda_0, s.exit, s.shape, 0)
                    s.passengerArrival = Model_Queue.mu(s.price, s.mu_0, s.shape)
                else:
                    s.price = p_high
                    s.driverArrival = Model_Queue.lambda_gamma(s.price, s.gamma, s.tau, s.lambda_0, s.exit, s.shape, 0)
                    s.passengerArrival = Model_Queue.mu(s.price, s.mu_0, s.shape)

            # Post-processing
            # Duplicates to drop as we would count the price multiple times for the same ride
            df.drop_duplicates(subset=['start'], keep=False, inplace=True)
            # Only use second half of the df
            # df.drop(df.head(int(len(df)/2)).index, inplace=True)
            df_result.loc[j, "Price i"] = i
            df_result.loc[j, "Time"] = s.clock
            df_result.loc[j, "Drivers arrived to system"] = s.arrivedDrivers
            df_result.loc[j, "Driver arrival rate | Agent"] = s.arrivedDrivers / s.clock
            df_result.loc[j, "Driver arrival rate | Theoretic"] = Model_Queue.lambda_dynamic(p_low, i, p_bal, mu_0,
                                                                                             q_exit, tau, gamma,
                                                                                             lambda_0, shape)
            df_result.loc[j, "Expected earnings per ride | Agent"] = np.average(df['price'])
            df_result.loc[j, "Expected earnings per ride | Theoretic"] = Model_Queue.Revenue_dynamic(p_low, i, p_bal,
                                                                                                     mu_0, q_exit, tau,
                                                                                                     lambda_0, shape,
                                                                                                     gamma, theta) / \
                                                                         df_result.loc[
                                                                             j, "Driver arrival rate | Theoretic"]
            df_result.loc[j, "Revenue | Agent"] = s.arrivedDrivers / s.clock * df_result.loc[j, "Expected earnings per ride | Agent"]
            df_result.loc[j, "Revenue | Theoretic"] = Model_Queue.Revenue_dynamic(p_low, p_high, p_bal, mu_0, q_exit, tau,
                                                                                  lambda_0, shape, gamma, theta)
            # Iterate
            j += 1

    # Check results for all iterations
    df_result.to_excel("result.xlsx")
    # Group multiple simulations m by price i
    if m != 1:
        df_ = df_result.groupby(df_result['Price i']).mean()
    else:
        df_ = df_result
    ### PLOT ###
    Model_Queue.plotDynamicAgentLambda(df_, p_max)
    Model_Queue.plotDynamicAgentRevenue(df_, p_max)
