import numpy as np
import scipy.stats
import matplotlib.pyplot as plt


### Passenger ###
# Estimation of mü
def mu(price, mu_0, shape):
    return mu_0 * passengerPriceResponse(price, shape)


# Ride-value distribution (passenger)
def passengerPriceResponse(price, shape):
    # Normal Distribution --- mean and standard deviation have to be specified
    # return (1-scipy.stats.norm.cdf(price, mean, std))
    # Gamma Distribution
    return 1 - scipy.stats.gamma.cdf(price, shape)


### Driver ###
# Normalized driver arrival rate --- large market limit ---
def lamlarge(price, gamma, tau, mu_0, bigLambda, q_exit, shape):
    m = mu(price, mu_0, shape)
    lam = bigLambda / q_exit * reservationEarningsDistr2(gamma / tau * price, shape)
    return min(lam, m)


def lam2(price, gamma, tau, bigLambda, q_exit, shape, idle):
    return bigLambda / q_exit * reservationEarningsDistr2((gamma * price) / (tau + idle), shape)


def dynamicLam(plow, phigh, pbal, mu_0, q_exit, tau, gamma, bigLambda, shape):
    if plow > pbal:
        return mu_0 * passengerPriceResponse(plow, shape)
    elif phigh < pbal:
        if phigh < plow:
            return lam2(plow, gamma, tau, bigLambda, q_exit, shape, 0)
        else:
            return lam2(phigh, gamma, tau, bigLambda, q_exit, shape, 0)
    elif plow < pbal < phigh:
        return lamThreshold(plow, phigh, tau, mu_0, gamma, bigLambda, q_exit, shape)


def lamThreshold(plow, phigh, tau, mu_0, gamma, bigLambda, q_exit, shape):
    phi_high = 1 / passengerPriceResponse(phigh, shape)
    phi_low = 1 / passengerPriceResponse(plow, shape)
    fac1 = bigLambda / q_exit
    fac2 = gamma / tau
    for i in np.arange(0.01, 10, 0.01):
        x = fac2 * ((plow * (phi_high - mu_0 / i) + phigh * (mu_0 / i - phi_low)) / (phi_high - phi_low))
        desc = fac1 * reservationEarningsDistr2(x, shape)
        if desc != 0 and np.absolute((i - desc) / i) <= 0.01:
            return desc
    return 1


### Driver ###
# Reservation-earnings distribution
def reservationEarningsDistr(gamma, tau, idle, price, shape):
    return scipy.stats.gamma.cdf((gamma * price) / (tau + idle), shape)


def reservationEarningsDistr2(earningsPerTime, shape):
    return scipy.stats.gamma.cdf(earningsPerTime, shape)


### Revenue ###
def dynamicRevenue(plow, p, p_bal, mu_0, q_exit, tau, bigLambda, shape, gamma, theta):
    lam = dynamicLam(plow, p, p_bal, mu_0, q_exit, tau, gamma, bigLambda, shape)
    eta = eta_(plow, p, lam, mu_0, theta, shape)
    if plow > p:
        return (1 - gamma) * lam * plow
    elif plow < p <= p_bal:
        return (1 - gamma) * lam * p
    else:
        return (1 - gamma) * lam * eta


def dynamicMultiplier(plow, p, p_bal, lam, mu_0, shape, gamma, theta):
    eta = eta_(plow, p, lam, mu_0, theta, shape)
    if plow > p:
        return (1 - gamma) * plow
    elif plow < p <= p_bal:
        return (1 - gamma) * p
    else:
        return (1 - gamma) * eta


### Prices ###
# Equation 8
def balancePriceStaticLarge(mu_0, gamma, tau, q_exit, bigLambda, shape):
    for i in np.arange(1, 10, 0.001):
        mu = mu_0 * passengerPriceResponse(i, shape)
        lam = (bigLambda / q_exit) * reservationEarningsDistr(gamma, tau, 0, i, shape)
        if mu != 0 and np.absolute((mu - lam) / mu) <= 0.001:
            return i
    return 0


def demandOptimalPrice(shape):
    opt = 0
    for i in np.arange(0.01, 10, 0.001):
        prod = i * passengerPriceResponse(i, shape)
        if prod > opt:
            opt = prod
        else:
            return i
    return 0


# Eta
def eta_(plow, phigh, lam, mu_0, theta, shape):
    rho_l = 1 / passengerPriceResponse(plow, shape)
    rho_h = 1 / passengerPriceResponse(phigh, shape)
    sig = lam / mu_0
    return (((sig * rho_h) ** theta - 1) * (1 - sig * rho_l) * phigh + (sig * rho_h - 1) * (
            (sig * rho_h) ** theta) * plow) / (
                   (sig * rho_h - sig * rho_l) * (sig * rho_h) ** theta - (1 - sig * rho_l))


### PLOTS ###
### Static large market limit | Theoretic
def plotStaticLambda(mu_0, gamma, tau, q_exit, bigLambda, shape, p_bal, pd_opt):
    x_end = 5
    y_end = 1.4
    x = np.linspace(0, x_end, 1000)
    y1 = (bigLambda / q_exit) * reservationEarningsDistr(gamma, tau, 0, x, shape)
    y2 = mu(x, mu_0, shape)
    plt.plot(x, y1, color='coral', label="$\\lambda$")
    plt.plot(x, y2, color='pink', label='$\\mu$')
    y3 = np.zeros(1000)
    j = 0
    for i in x:
        y3[j] = lamlarge(i, gamma, tau, mu_0, bigLambda, q_exit, shape)
        j = j + 1
    plt.plot(x, y3, color='green', linestyle='dotted', linewidth=3.0, label="$\\lambda_{fin}$")
    plt.vlines(p_bal, 0, y_end, colors='black', linestyles='solid', label='Balance Price')
    plt.vlines(pd_opt, 0, y_end, colors='grey', linestyles='dashed', label='Optimal Price')
    plt.grid()
    plt.xlim(0, x_end)
    plt.ylim(0, y_end)
    plt.xlabel('Price')
    plt.ylabel('$\\lambda$(n,p)')
    plt.legend()
    plt.title("Static large market limit: \n" "$\\lambda$(p) vs p ")
    plt.savefig("Plots/LargeMarketLimit_static_lambda")
    plt.show()


def plotStaticRevenue(mu_0, gamma, tau, q_exit, bigLambda, shape, p_bal, pd_opt):
    x_end = 5
    y_end = 3.2
    x = np.linspace(0, x_end, 1000)
    y1 = np.zeros(1000)
    j = 0
    for i in x:
        y1[j] = lamlarge(i, gamma, tau, mu_0, bigLambda, q_exit, shape) * i * (1 - gamma)
        j = j + 1
    plt.plot(x, y1, color='coral', label="Revenue")
    plt.vlines(p_bal, 0, y_end, colors='black', linestyles='solid', label='$p_{bal}$')
    plt.vlines(pd_opt, 0, y_end, colors='grey', linestyles='dashed', label='$p_{opt}$')
    plt.grid()
    plt.xlim(0, x_end)
    plt.ylim(0, y_end)
    plt.xlabel('Price')
    plt.ylabel('Revenue')
    plt.legend()
    plt.title("Static large market limit Revenue: \n E[$\\Pi$(p)] vs. p, $\\gamma$=0")
    plt.savefig("Plots/LargeMarketLimit_Revenue")
    plt.show()


### Static large market limit | Agent
def plotAgentLam(df_result, p_max):
    plt.plot(df_result['Price'], df_result['Driver arrival agent based'], color='red', label="$\\lambda_{agent}$")
    plt.plot(df_result['Price'], df_result['Driver arrival paper'], color='green', linestyle='dashed',
             label="$\\lambda_{theoretic}$")
    plt.grid()
    plt.xlim(0, p_max)
    plt.ylim(0, 1.4)
    plt.xlabel('Price')
    plt.ylabel('Driver arrival rate')
    plt.legend()
    plt.title("Static large market limit agent based:\n $F_C, F_V$ ~ Gamma(2,0)")
    plt.savefig("Plots/Arrival_rate_avg")
    plt.show()


def plotAgentRev(df_result, p_max):
    plt.plot(df_result['Price'], df_result['Revenue agent based per ride'], color='red', label="$Revenue_{agent}$")
    plt.plot(df_result['Price'], df_result['Revenue paper'], color='green', linestyle='dashed',
             label="$Revenue_{theoretic}$")
    plt.grid()
    plt.xlim(0, p_max)
    plt.ylim(0, 3.5)
    plt.xlabel('Price')
    plt.ylabel('Revenue')
    plt.legend()
    plt.title("Static large market limit agent based:\n $F_C, F_V$ ~ Gamma(2,0), $\\gamma$ = 0")
    plt.savefig("Plots/Revenue_avg")
    plt.show()


### Dynamic large amrket limit | Agent
def plotAgentDynLam(df_result, p_max):
    plt.plot(df_result['Price'], df_result['Driver arrival agent based'], color='red', label="$\\lambda_{agent}$")
    plt.plot(df_result['Price'], df_result['Driver arrival paper'], color='green', linestyle='dashed',
             label="$\\lambda_{theoretic}$")
    plt.grid()
    plt.xlim(0, p_max)
    plt.ylim(0, 1.4)
    plt.xlabel('Price', fontsize=12)
    plt.ylabel('$\\lim_{n\\to\\infty} \\lambda$(n,p)', fontsize=12)
    plt.legend()
    plt.title("Dynamic Large Market Limit | Agent: \n""$\\lambda$(n,p) vs. p")
    plt.savefig("Plots/Dynamic_Agent_lam")
    plt.show()


def plotAgentDynRev(df_result, p_max):
    plt.plot(df_result['Price'], df_result['Revenue agent based per ride'], color='red', label="$Revenue_{agent}$")
    plt.plot(df_result['Price'], df_result['Revenue paper'], color='green', linestyle='dashed',
             label="$Revenue_{theoretic}$")
    plt.grid()
    plt.xlim(0, p_max)
    plt.ylim(0, 3.5)
    plt.xlabel('Price')
    plt.ylabel('Revenue')
    plt.legend()
    plt.title("Dynamic Large Market Limit | Agent: \n E[$\\Pi$(p)] vs. p, $\\gamma$=0")
    plt.savefig("Plots/Dynamic_Agent_Revenue_avg")
    plt.show()


### Dynamic single threshold pricing vs. static pricing | Theoretic
def plotPriceLambdaDyn(mu_0, gamma, tau, q_exit, bigLambda, shape, p_bal, plow):
    x_end = 5
    y_end = 1.6
    x = np.linspace(0, x_end, 1000)
    y1 = np.zeros(1000)
    j = 0
    for i in x:
        y1[j] = dynamicLam(plow, i, p_bal, mu_0, q_exit, tau, gamma, bigLambda, shape)
        j = j + 1
    y2 = np.zeros(1000)
    j = 0
    for i in x:
        y2[j] = lamlarge(i, gamma, tau, mu_0, bigLambda, q_exit, shape)
        j = j + 1
    plt.plot(x, y2, color='green', label="Static pricing")
    plt.plot(x, y1, color='red', label='Dynamic pricing')
    plt.vlines(p_bal, 0, y_end, colors='black', linestyles='solid', label='$p_{bal}$')
    plt.vlines(plow, 0, y_end, colors='yellow', linestyles='solid', label='$p_{low}$')
    plt.grid()
    plt.xlim(0, x_end)
    plt.ylim(0, y_end)
    plt.xlabel('Price', fontsize=12)
    plt.ylabel('$\\lim_{n\\to\\infty} \\lambda$(n,p)', fontsize=12)
    plt.legend()
    plt.title("Large Market Limits under Static and Dynamic Pricing: \n""$\\lambda$(n,p) vs. p")
    plt.savefig("Plots/LargeMarketLimit_Dynamic_Lambda")
    plt.show()


def plotRevenueDynStat(mu_0, gamma, tau, q_exit, bigLambda, shape, p_bal, plow, theta):
    x_end = 5
    y_end = 3.2
    x = np.linspace(0, x_end, 1000)
    y1 = np.zeros(1000)
    j = 0
    for i in x:
        y1[j] = lamlarge(i, gamma, tau, mu_0, bigLambda, q_exit, shape) * i * (1 - gamma)
        j = j + 1
    plt.plot(x, y1, color='green', label="Static pricing")
    y3 = np.zeros(1000)
    j = 0
    for i in x:
        y3[j] = dynamicRevenue(plow, i, p_bal, mu_0, q_exit, tau, bigLambda, shape, gamma, theta)
        y3[j] = dynamicRevenue(plow, i, p_bal, mu_0, q_exit, tau, bigLambda, shape, gamma, theta)
        j = j + 1
    plt.plot(x, y3, color='red', label="Dynamic Pricing")
    plt.vlines(p_bal, 0, y_end, colors='black', linestyles='solid', label='$p_{bal}$')
    plt.vlines(plow, 0, y_end, colors='yellow', label='$p_{low}$')
    plt.grid()
    plt.xlim(0, x_end)
    plt.ylim(0, y_end)
    plt.xlabel('Price')
    plt.ylabel('Revenue')
    plt.legend()
    plt.title("Large Market Limits Revenue under Static and Dynamic Pricing: \n E[$\\Pi$(p)] vs. p, $\\gamma$=0")
    plt.savefig("Plots/LargeMarketLimit_Revenue_Dyn_vs_Stat")
    plt.show()
