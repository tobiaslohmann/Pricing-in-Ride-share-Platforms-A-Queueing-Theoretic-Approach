import numpy as np
import Model_Queue
import static_simulation


class Simulation:
    def __init__(self, p_high, p_low, p_bal, mu_0, q_exit, tau, gamma, lambda_0, shape):
        self.clock = 0.0                    # simulation clock
        self.start = 0                      # start of ride
        self.end = 0                        # end of ride
        self.queue_p = 0                    # Passenger queue size
        self.queue_d = 0                    # Driver queue size
        self.mu_0 = mu_0                    # Potential ride request
        self.shape = shape                  # Shape GAMMA
        self.exit = q_exit                  # Exit probability
        self.balance = p_bal                # Balance price
        self.tau = tau                      # Service time
        self.gamma = gamma                  # Fraction driver earns
        self.lambda_0 = lambda_0            # Potential new drivers
        self.p_low = p_low                  # Low price
        self.price = p_high                 # High price
        self.p_arrival = self.arrive_p()    # Time of next passenger arrival
        self.d_arrival = self.arrive_d()    # Time of next driver arrival
        self.driverArrival = 0              # Driver arrival rate | Theoretic
        self.passengerArrival = 0           # Passenger arrival rate | Theoretic
        self.arrivedDrivers = 0             # Drivers arrived to system at time clock

    def time(self):
        t_next_event = min(self.p_arrival, self.d_arrival)
        self.clock = t_next_event
        if self.d_arrival < self.p_arrival:
            self.arrival_d()
        else:
            self.arrival_p()

    def arrival_p(self):
        # Passenger queue empty
        if self.queue_p == 0:
            # No driver available
            if self.queue_d == 0:
                self.queue_p += 1
                # Set time for next arrival
                self.p_arrival = self.clock + self.arrive_p()
            # Driver available
            else:
                self.queue_d -= 1
                self.start = self.clock
                self.end = self.clock + static_simulation.serviceTime()
                # Set time for next arrival
                self.p_arrival = self.clock + self.arrive_p()
        else:
            self.queue_p += 1
            # Set time for next arrival
            self.p_arrival = self.clock + self.arrive_p()

    def arrival_d(self):
        self.arrivedDrivers += 1
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
                self.end = self.clock + static_simulation.serviceTime()
                # Set time for next arrival
                self.d_arrival = self.clock + self.arrive_d()
        else:
            self.queue_d += 1
            # Set time for next arrival
            self.d_arrival = self.clock + self.arrive_d()

    def arrive_p(self):
        rng = np.random.default_rng()
        mu = Model_Queue.mu(self.price, self.mu_0, self.shape)
        return rng.exponential(scale=1.0 / mu)

    def arrive_d(self):
        rng = np.random.default_rng()
        lam = Model_Queue.lambda_gamma(self.price, self.gamma, self.tau, self.lambda_0, self.exit,
                                       self.shape, 0)
        return rng.exponential(scale=1.0 / lam)
