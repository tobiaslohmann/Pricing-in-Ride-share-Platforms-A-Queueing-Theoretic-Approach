import numpy as np
import pandas as pd

rng = np.random.default_rng()

def simulation(df_p, df_d, n, d_arrival_rate, p_arrival_rate, price, gamma):
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
        "driverArrivalRate": d_arrival_rate,
        "passengerArrivalRate": p_arrival_rate,
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
    # service time = "exponential length of time with mean tau"
    # 1/10 = 6min as average mean is used. --- Won't change the outcome of the model
    return rng.exponential(scale=1.0 / 10)
