import Model_Queue


def main(mu_0, q_exit, bigLambda, gamma, tau, shape):
    ### Estimating balance price and demand optimal price ###
    pbal = Model_Queue.balancePriceStaticLarge(mu_0, gamma, tau, q_exit,
                                               bigLambda, shape)
    pd_opt = Model_Queue.demandOptimalPrice(shape)
    if pbal >= pd_opt:
        price = pbal
    else:
        price = pd_opt
    passengerArrival = Model_Queue.mu(price, mu_0, shape)
    driverArrival = Model_Queue.lamlarge(price, gamma, tau, mu_0,
                                         bigLambda, q_exit, shape)
    ### OUTPUT ###
    print("Balance Price - Equilibrium: ", pbal)
    print("Optimal Price - Non strategic driver: ", pd_opt)
    print("Arrival rate passengers: ", passengerArrival)
    print("Arrival rate drivers: ", driverArrival)

    ### PLOT ###
    Model_Queue.plotStaticLambda(mu_0, gamma, tau, q_exit, bigLambda, shape, pbal, pd_opt)
    Model_Queue.plotStaticRevenue(mu_0, gamma, tau, q_exit, bigLambda, shape, pbal, pd_opt)
