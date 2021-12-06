import numpy as np
import pandas as pd
import Model_Queue
import agentSimulation

class Bank_Simulation:
    def __init__(self, phigh, plow, pbal, mu_0, q_exit, tau, gamma, bigLambda, shape):
        self.clock = 0.0  # simulation clock
        self.num_arrivals = 0  # total number of arrivals
        self.start = 0  # start of ride
        self.end = 0    # end of ride
        self.queue_p = 0  # current number in queue
        self.queue_d = 0
        self.price = 0  # current price
        self.mu_0 = mu_0  # mu_0 given from the paper
        self.shape = shape
        self.exit = q_exit
        self.balance = pbal
        self.tau = tau
        self.gamma = gamma
        self.bigLambda = bigLambda
        self.price_low = plow
        self.price = phigh
        self.p_arrival = self.arrive_p()  # time of next passenger arrival
        self.d_arrival = self.arrive_d()  # time of next driver arrival

    def to_list(self):
        return [self.clock, self.p_arrival, self.d_arrival, self.queue_p, self.queue_d, self.start, self.end]


    def time_adv(self):
        t_next_event = min(self.p_arrival, self.d_arrival)
        self.clock = t_next_event
        if self.d_arrival < self.p_arrival:
            self.arrival_d()
        else:
            self.arrival_p()

    def arrival_p(self):
        self.num_arrivals += 1

        # Passenger queue empty
        if self.queue_p == 0:
            # No driver available
            if self.queue_d == 0:
                self.queue_p += 1
                # Set time for next arrival
                self.p_arrival = self.clock + self.arrive_p()
            # Driver available
            else:
                self.queue_d -=1
                self.start = self.clock
                self.end = self.clock + agentSimulation.serviceTime()
                # Set time for next arrival
                self.p_arrival = self.clock + self.arrive_p()
        else:
            self.queue_p +=1
            # Set time for next arrival
            self.p_arrival = self.clock + self.arrive_p()

    def arrival_d(self):
        # Driver queue is empty
        if self.queue_d == 0:
            # No passenger available
            if self.queue_p == 0:
                self.queue_d += 1
                # Set time for next arrival
                self.d_arrival = self.clock + self.arrive_d()
            # Passenger available
            else:
                self.queue_p -= 1
                self.start = self.clock
                self.end = self.clock + agentSimulation.serviceTime()
                # Set time for next arrival
                self.d_arrival = self.clock + self.arrive_d()
        else:
            self.queue_d += 1
            # Set time for next arrival
            self.d_arrival = self.clock + self.arrive_d()

    def arrive_p(self):
        rng = np.random.default_rng()
        mu =  Model_Queue.mu(self.price, self.mu_0, self.shape)
        return rng.exponential(scale=1.0 / mu, size=1)

    def arrive_d(self):
        rng = np.random.default_rng()
        lam =  Model_Queue.dynamicLam(self.price_low, self.price, self.balance, self.mu_0, self.exit, self.tau, self.gamma, self.bigLambda, self.shape)
        return rng.exponential(scale=1.0 / lam, size=1)



if __name__ == '__main__':
    mu_0 = 4
    shape = 2
    pbal = 2.3
    plow = 0.75 * pbal
    # Theta in the  large market limit: n goes to infinity
    theta_0 = 3
    n = 10000000000000000000
    theta = theta_0 * np.log(n)
    # price to set (variate)
    phigh = 4
    q_exit = 0.5
    bigLambda = 1
    tau = 0.000000000001
    gamma = 0.000000000001
    s = Bank_Simulation(phigh, plow, pbal, mu_0, q_exit, tau, gamma, bigLambda, shape)
    df = pd.DataFrame(
        columns=['Clock', 'passenger Arrival', 'driver Arrival',
                 'passenger queue', 'driver queue', 'start',
                 'end', 'price'])
    np.random.seed()
    s.__init__(phigh, plow, pbal, mu_0, q_exit, tau, gamma, bigLambda, shape)
    while s.clock <= 240:
        s.time_adv()
        df = df.append(pd.Series([s.clock, s.p_arrival, s.d_arrival, s.queue_p, s.queue_d, s.start, s.end, s.price], index=df.columns), ignore_index=True)
        if s.queue_d > theta:
            s.price = plow
        else:
            s.price = phigh

    print(s.to_list())
    df.to_excel("result.xlsx")
    # a = pd.Series([s.clock / s.num_arrivals, s.dep_sum1 / s.num_of_departures1, s.dep_sum2 / s.num_of_departures2,
    #                s.dep_sum1 / s.clock, s.dep_sum2 / s.clock, s.number_in_queue, s.total_wait_time,
    #                s.lost_customers],
    #               index=df.columns)
    # df = df.append(a, ignore_index=True)
