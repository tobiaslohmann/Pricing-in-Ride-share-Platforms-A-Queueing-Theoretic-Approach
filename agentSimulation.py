import numpy as np
import pandas as pd

# specify a seed so that we have reproducible results
rng = np.random.default_rng()


def simulationStatic(df_p, df_d, n, driverArrival, passengerArrival, price, gamma):
    ### Pre-processing ###
    # Create df of size n - n is defined in main
    result_df = pd.DataFrame({
        "arrive_time_passenger": np.zeros(n),
        "available_time_driver": np.zeros(n),
        "service_time": np.zeros(n),
        "time_in_system_passenger": np.zeros(n),
        "waiting_time_passenger": np.zeros(n),
        "idle_time_driver": np.zeros(n),
        "start_time": np.zeros(n),
        "depart_time": np.zeros(n),
        "driverArrivalRate": driverArrival,
        "passengerArrivalRate": passengerArrival,
        "Price": price,
        "Revenue": price * (1 - gamma)
    })
    ### Simulation ###
    for i in range(0, n):
        result_df.loc[i, "arrive_time_passenger"] = df_p.loc[i, "arrival_times"]
        result_df.loc[i, "available_time_driver"] = df_d.loc[i, "arrival_times"]
        result_df.loc[i, "service_time"] = serviceTime()
        result_df.loc[i, "waiting_time_passenger"] = max(0, df_d.loc[i, "arrival_times"] - df_p.loc[i, "arrival_times"])
        result_df.loc[i, "idle_time_driver"] = max(0, df_p.loc[i, "arrival_times"] - df_d.loc[i, "arrival_times"])
        result_df.loc[i, "start_time"] = max(df_d.loc[i, "arrival_times"], df_p.loc[i, "arrival_times"])
        result_df.loc[i, "depart_time"] = result_df.loc[i, "start_time"] + result_df.loc[i, "service_time"]
        result_df.loc[i, "time_in_system_passenger"] = result_df.loc[i, "depart_time"] - result_df.loc[
            i, "arrive_time_passenger"]
        ### Time Analysis ###
        # if claused can be used to run simulation alway for the same timeframe and NOT dependent on matches
        # if result_df.loc[i, "start_time"] > 2400:
        #     break
    return result_df


def simulationDynamic(df_p, df_d, n, driverArrival, passengerArrival, price, gamma):
    ### Pre-processing ###
    # Create df of size n - n is defined in main
    result_df = pd.DataFrame({
        "arrive_time_passenger": np.zeros(n),
        "available_time_driver": np.zeros(n),
        "service_time": np.zeros(n),
        "time_in_system_passenger": np.zeros(n),
        "waiting_time_passenger": np.zeros(n),
        "idle_time_driver": np.zeros(n),
        "start_time": np.zeros(n),
        "depart_time": np.zeros(n),
        "driverArrivalRate": driverArrival,
        "passengerArrivalRate": passengerArrival,
        "Price": price,
        "Revenue": price * (1 - gamma)
    })
    ### Simulation ###
    for i in range(0, n):
        result_df.loc[i, "arrive_time_passenger"] = df_p.loc[i, "arrival_times"]
        result_df.loc[i, "available_time_driver"] = df_d.loc[i, "arrival_times"]
        result_df.loc[i, "service_time"] = serviceTime()
        result_df.loc[i, "waiting_time_passenger"] = max(0, df_d.loc[i, "arrival_times"] - df_p.loc[i, "arrival_times"])
        result_df.loc[i, "idle_time_driver"] = max(0, df_p.loc[i, "arrival_times"] - df_d.loc[i, "arrival_times"])
        result_df.loc[i, "start_time"] = max(df_d.loc[i, "arrival_times"], df_p.loc[i, "arrival_times"])
        result_df.loc[i, "depart_time"] = result_df.loc[i, "start_time"] + result_df.loc[i, "service_time"]
        result_df.loc[i, "time_in_system_passenger"] = result_df.loc[i, "depart_time"] - result_df.loc[
            i, "arrive_time_passenger"]
        ### Time Analysis ###
        # if claused can be used to run simulation alway for the same timeframe and NOT dependent on matches
        if result_df.loc[i, "start_time"] > 2400:
            break
    return result_df


def create_df(n, mean_arrival_rate):
    ### Poisson Arrival process ###
    # Compute interarrival times and arrival_times as the cumsum
    interarrival_times = rng.exponential(scale=1.0 / mean_arrival_rate, size=n)
    arrival_times = np.cumsum(interarrival_times)
    df = pd.DataFrame({
        "interarrival_times": interarrival_times,
        "arrival_times": arrival_times
    })
    return df


def serviceTime():
    # specify a seed so that we have reproducible results
    rng_ = np.random.default_rng()
    # scale parameter could be chosen randomly as well
    # Paper: "exponential length of time with mean tau"
    # As Tau = 0.00000001 as gamma = 0 and gamma/tau = 1, it does not make sense to pick 0 as service time
    # Hence, 1/10 = 6min as average mean is used. --- Can be changed for further analysis
    return rng_.exponential(scale=1.0 / 10, size=1)
