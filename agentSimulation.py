import numpy as np
import pandas as pd
import Model_Queue

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


def simulationDynamic(df_p, df_d, n, driverArrival, passengerArrival, price, pbal, plow, gamma, theta, mu_0, qexit, tau,
                      bigLambda, shape):
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
        "driverArrivalRate": np.zeros(n),
        "passengerArrivalRate": np.zeros(n),
        "Price": np.zeros(n),
        "Revenue": np.zeros(n),
        "Queue_length_driver": np.zeros(n)
    })
    p = price
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
        result_df.loc[i, "driverArrivalRate"] = driverArrival
        result_df.loc[i, "passengerArrivalRate"] = driverArrival
        result_df.loc[i, "Price"] = p
        result_df.loc[i, "Price"] = p * (1 - gamma)
        # Events
        if i % 10 ==0:
            if i ==0:
                events = build_events_df_d(i + 1, result_df,0, 0, 0, 0, 0)
            else:
                events = build_events_df_d(i + 1, result_df, arrive_idx, start_idx, depart_idx, num_system, num_queue)
            arrive_idx = events[0]
            start_idx = events[1]
            depart_idx = events[2]
            num_system = events[3]
            num_queue = events[4]
            result_df.loc[i, "Queue_length_driver"] = num_queue
            print(events)
            print(i, "  ", p, "    ", result_df.loc[i, "Queue_length_driver"])
        # Higher than threshold --> low price
        if p > pbal and num_queue > theta:
            p = plow
            passengerArrival = Model_Queue.mu(p, mu_0, shape)
            driverArrival = Model_Queue.dynamicLam(plow, p, pbal, mu_0, qexit, tau, gamma, bigLambda, shape)
            df_p = create_df(n, passengerArrival)
            df_d = create_df(n, driverArrival)
        # Lower threshold --> high price
        elif p == plow and num_queue < theta:
            p = price
            passengerArrival = Model_Queue.mu(p, mu_0, shape)
            driverArrival = Model_Queue.dynamicLam(plow, p, pbal, mu_0, qexit, tau, gamma, bigLambda, shape)
            df_p = create_df(n, passengerArrival)
            df_d = create_df(n, driverArrival)

            # Time Analysis
        # if clause can be used to run simulation alway for the same timeframe and NOT dependent on matches
        # if result_df.loc[i, "start_time"] > 2400:
        #     break
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


def build_events_df_d(n, jobs_df, arrive_idx, start_idx, depart_idx, num_system, num_queue):
    n = n
    arrivals = jobs_df["available_time_driver"]
    starts = jobs_df["start_time"]
    departures = jobs_df["depart_time"]

    # width = up_bd - lo_bd, num_jobs_in_queue = num_jobs_in_system - 1
    events_df = pd.DataFrame(columns=["lo_bd", "up_bd", "width", "num_jobs_in_system", "num_drivers_in_queue"])

    arrive_idx = arrive_idx
    start_idx = start_idx
    depart_idx = depart_idx
    num_jobs_in_system = num_system
    num_jobs_in_queue = num_queue

    while depart_idx < n:
        arrival = arrivals[arrive_idx] if arrive_idx < n else float("inf")
        start = starts[start_idx] if start_idx < n else float("inf")
        departure = departures[depart_idx]

        # Arrival job in system --> one more for system(+1) and one more for queue(+1)
        if arrival <= start and arrival <= departure:
            up_bd = arrival
            n_change, nq_change = 1, 1
            arrive_idx = arrive_idx + 1
        # Matching but still in service --> left from queue(-1) but still in system(+-0)
        elif start <= arrival and start <= departure:
            up_bd = start
            n_change, nq_change = 0, -1
            start_idx = start_idx + 1
        # Departure from the system --> in service not queue (+-0) but leave from system (-1)
        else:
            up_bd = departure
            n_change, nq_change = -1, 0
            depart_idx = depart_idx + 1

        events_df = events_df.append({
            "up_bd": up_bd,
            "num_jobs_in_system": num_jobs_in_system,
            "num_drivers_in_queue": num_jobs_in_queue,
            "num_jobs_in_system_change": n_change,
            "num_jobs_in_queue_change": nq_change,
        }, ignore_index=True)

        num_jobs_in_system = num_jobs_in_system + n_change
        num_jobs_in_queue = num_jobs_in_queue + nq_change

    return [arrive_idx, start_idx, depart_idx, num_jobs_in_system, num_jobs_in_queue]
