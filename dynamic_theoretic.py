import Model_Queue


def main(mu_0, q_exit, lambda_0, gamma, tau, shape, theta):
    ### Estimating balance price and demand optimal price ###
    p_bal = Model_Queue.balance_price(mu_0, gamma, tau, q_exit, lambda_0, shape)
    pd_opt = Model_Queue.optimal_price(shape)
    if p_bal >= pd_opt:
        price = p_bal
    else:
        price = pd_opt
    p_arrival_rate = Model_Queue.mu(price, mu_0, shape)
    d_arrival_rate = Model_Queue.lambda_static(price, gamma, tau, mu_0, lambda_0, q_exit, shape)
    # Given from the paper
    p_low = price * 0.75
    ### OUTPUT ###
    print("Balance Price - Equilibrium: ", p_bal)
    print("Optimal Price - Non strategic driver: ", pd_opt)
    print("Arrival rate passengers: ", p_arrival_rate)
    print("Arrival rate drivers: ", d_arrival_rate)

    ### PLOT ###
    Model_Queue.plotPriceLambdaDyn(mu_0, gamma, tau, q_exit, lambda_0, shape, p_bal, p_low)
    Model_Queue.plotRevenueDynStat(mu_0, gamma, tau, q_exit, lambda_0, shape, p_bal, p_low, theta)
