import Model_Queue


def main(mu_0, q_exit, bigLambda, gamma, tau, shape, theta):
    ### Estimating balance price and demand optimal price ###
    pBal = Model_Queue.balancePriceStaticLarge(mu_0, gamma, tau, q_exit,
                                               bigLambda, shape)
    pd_opt = Model_Queue.demandOptimalPrice(shape)
    if pBal >= pd_opt:
        price = pBal
    else:
        price = pd_opt
    passengerArrival = Model_Queue.mu(price, mu_0, shape)
    driverArrival = Model_Queue.lamlarge(price, gamma, tau, mu_0,
                                         bigLambda, q_exit, shape)
    # Given from the paper
    plow = price * 0.75
    ### OUTPUT ###
    print("Balance Price - Equilibrium: ", pBal)
    print("Optimal Price - Non strategic driver: ", pd_opt)
    print("Arrival rate passengers: ", passengerArrival)
    print("Arrival rate drivers: ", driverArrival)

    ### PLOT ###
    Model_Queue.plotPriceLambdaDyn(mu_0, gamma, tau, q_exit, bigLambda, shape, pBal, plow)
    Model_Queue.plotRevenueDynStat(mu_0, gamma, tau, q_exit, bigLambda, shape, pBal, plow, theta)
