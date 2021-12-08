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
def lambda_static(price, gamma, tau, mu_0, lambda_0, q_exit, shape):
    m = mu(price, mu_0, shape)
    lam = lambda_0 / q_exit * reservation_earnings_distribution_eta(gamma / tau * price, shape)
    return min(lam, m)


def lambda_gamma(price, gamma, tau, lambda_0, q_exit, shape, idle):
    return lambda_0 / q_exit * reservation_earnings_distribution_eta((gamma * price) / (tau + idle), shape)


def lambda_dynamic(p_low, p_high, p_bal, mu_0, q_exit, tau, gamma, lambda_0, shape):
    if p_low > p_bal:
        return mu_0 * passengerPriceResponse(p_low, shape)
    elif p_high < p_bal:
        if p_high < p_low:
            return lambda_gamma(p_low, gamma, tau, lambda_0, q_exit, shape, 0)
        else:
            return lambda_gamma(p_high, gamma, tau, lambda_0, q_exit, shape, 0)
    elif p_low < p_bal < p_high:
        return lambda_threshold(p_low, p_high, tau, mu_0, gamma, lambda_0, q_exit, shape)


def lambda_threshold(p_low, p_high, tau, mu_0, gamma, lambda_0, q_exit, shape):
    phi_high = 1 / passengerPriceResponse(p_high, shape)
    phi_low = 1 / passengerPriceResponse(p_low, shape)
    fac1 = lambda_0 / q_exit
    fac2 = gamma / tau
    for i in np.arange(0.01, 10, 0.01):
        x = fac2 * ((p_low * (phi_high - mu_0 / i) + p_high * (mu_0 / i - phi_low)) / (phi_high - phi_low))
        desc = fac1 * reservation_earnings_distribution_eta(x, shape)
        if desc != 0 and np.absolute((i - desc) / i) <= 0.01:
            return desc
    return 1


### Driver ###
# Reservation-earnings distribution
def reservation_earnings_distribution(gamma, tau, idle, price, shape):
    return scipy.stats.gamma.cdf((gamma * price) / (tau + idle), shape)


def reservation_earnings_distribution_eta(earningsPerTime, shape):
    return scipy.stats.gamma.cdf(earningsPerTime, shape)


### Revenue ###
def Revenue_dynamic(p_low, p, p_bal, mu_0, q_exit, tau, lambda_0, shape, gamma, theta):
    lam = lambda_dynamic(p_low, p, p_bal, mu_0, q_exit, tau, gamma, lambda_0, shape)
    eta = eta_(p_low, p, lam, mu_0, theta, shape)
    if p_low >= p:
        return (1 - gamma) * lam * p_low
    elif p_low < p <= p_bal:
        return (1 - gamma) * lam * p
    else:
        return (1 - gamma) * lam * eta

### Prices ###
# Equation 8
def balance_price(mu_0, gamma, tau, q_exit, lambda_0, shape):
    for i in np.arange(1, 10, 0.001):
        mu = mu_0 * passengerPriceResponse(i, shape)
        lam = (lambda_0 / q_exit) * reservation_earnings_distribution(gamma, tau, 0, i, shape)
        if mu != 0 and np.absolute((mu - lam) / mu) <= 0.001:
            return i
    return 0


def optimal_price(shape):
    opt = 0
    for i in np.arange(0.01, 10, 0.001):
        prod = i * passengerPriceResponse(i, shape)
        if prod > opt:
            opt = prod
        else:
            return i
    return 0


# Eta
def eta_(p_low, p_high, lam, mu_0, theta, shape):
    rho_l = 1 / passengerPriceResponse(p_low, shape)
    rho_h = 1 / passengerPriceResponse(p_high, shape)
    sig = lam / mu_0
    return (((sig * rho_h) ** theta - 1) * (1 - sig * rho_l) * p_high + (sig * rho_h - 1) * (
            (sig * rho_h) ** theta) * p_low) / (
                   (sig * rho_h - sig * rho_l) * (sig * rho_h) ** theta - (1 - sig * rho_l))


### PLOTS ###
### Static large market limit | Theoretic
def plotStaticLambda(mu_0, gamma, tau, q_exit, lambda_0, shape, p_bal, pd_opt):
    x_end = 5
    y_end = 1.4
    x = np.linspace(0, x_end, 1000)
    y1 = (lambda_0 / q_exit) * reservation_earnings_distribution(gamma, tau, 0, x, shape)
    y2 = mu(x, mu_0, shape)
    plt.plot(x, y1, color='coral', label="$\\lambda$")
    plt.plot(x, y2, color='pink', label='$\\mu$')
    y3 = np.zeros(1000)
    j = 0
    for i in x:
        y3[j] = lambda_static(i, gamma, tau, mu_0, lambda_0, q_exit, shape)
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
    plt.savefig("Static/Static_Theoretic_Lambda")
    plt.show()


def plotStaticRevenue(mu_0, gamma, tau, q_exit, lambda_0, shape, p_bal, pd_opt):
    x_end = 5
    y_end = 3.2
    x = np.linspace(0, x_end, 1000)
    y1 = np.zeros(1000)
    j = 0
    for i in x:
        y1[j] = lambda_static(i, gamma, tau, mu_0, lambda_0, q_exit, shape) * i * (1 - gamma)
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
    plt.savefig("Static/Static_Theoretic_Revenue")
    plt.show()


### Static large market limit | Agent
def plotStaticAgentLambda(df_result, p_max):
    plt.plot(df_result['Price'], df_result['Driver arrival rate | Agent'], color='red', label="$\\lambda_{agent}$")
    plt.plot(df_result['Price'], df_result['Driver arrival rate | Theoretic'], color='green', linestyle='dashed',
             label="$\\lambda_{theoretic}$")
    plt.grid()
    plt.xlim(0, p_max)
    plt.ylim(0, 1.4)
    plt.xlabel('Price')
    plt.ylabel('Driver arrival rate')
    plt.legend()
    plt.title("Static large market limit agent based:\n $F_C, F_V$ ~ Gamma(2,0)")
    plt.savefig("Static/Static_Agent_Lambda")
    plt.show()


def plotStaticAgentRevenue(df_result, p_max):
    plt.plot(df_result['Price'], df_result['Revenue | Agent'], color='red', label="$Revenue_{agent}$")
    plt.plot(df_result['Price'], df_result['Revenue | Theoretic'], color='green', linestyle='dashed',
             label="$Revenue_{theoretic}$")
    plt.grid()
    plt.xlim(0, p_max)
    plt.ylim(0, 3.5)
    plt.xlabel('Price')
    plt.ylabel('Revenue')
    plt.legend()
    plt.title("Static large market limit agent based:\n $F_C, F_V$ ~ Gamma(2,0), $\\gamma$ = 0")
    plt.savefig("Static/Static_Agent_Revenue_avg")
    plt.show()


### Dynamic single threshold pricing vs. static pricing | Theoretic
def plotPriceLambdaDyn(mu_0, gamma, tau, q_exit, lambda_0, shape, p_bal, p_low):
    x_end = 5
    y_end = 1.6
    x = np.linspace(0, x_end, 1000)
    y1 = np.zeros(1000)
    j = 0
    for i in x:
        y1[j] = lambda_dynamic(p_low, i, p_bal, mu_0, q_exit, tau, gamma, lambda_0, shape)
        j = j + 1
    y2 = np.zeros(1000)
    j = 0
    for i in x:
        y2[j] = lambda_static(i, gamma, tau, mu_0, lambda_0, q_exit, shape)
        j = j + 1
    plt.plot(x, y2, color='green', label="Static pricing")
    plt.plot(x, y1, color='red', label='Dynamic pricing')
    plt.vlines(p_bal, 0, y_end, colors='black', linestyles='solid', label='$p_{bal}$')
    plt.vlines(p_low, 0, y_end, colors='yellow', linestyles='solid', label='$p_{low}$')
    plt.grid()
    plt.xlim(0, x_end)
    plt.ylim(0, y_end)
    plt.xlabel('Price', fontsize=12)
    plt.ylabel('$\\lim_{n\\to\\infty} \\lambda$(n,p)', fontsize=12)
    plt.legend()
    plt.title("Large Market Limits under Static and Dynamic Pricing: \n""$\\lambda$(n,p) vs. p")
    plt.savefig("Dynamic/Dynamic_Theoretic_Lambda")
    plt.show()


def plotRevenueDynStat(mu_0, gamma, tau, q_exit, lambda_0, shape, p_bal, p_low, theta):
    x_end = 5
    y_end = 3.2
    x = np.linspace(0, x_end, 1000)
    y1 = np.zeros(1000)
    j = 0
    for i in x:
        y1[j] = lambda_static(i, gamma, tau, mu_0, lambda_0, q_exit, shape) * i * (1 - gamma)
        j = j + 1
    plt.plot(x, y1, color='green', label="Static pricing")
    y3 = np.zeros(1000)
    j = 0
    for i in x:
        y3[j] = Revenue_dynamic(p_low, i, p_bal, mu_0, q_exit, tau, lambda_0, shape, gamma, theta)
        j = j + 1
    plt.plot(x, y3, color='red', label="Dynamic Pricing")
    plt.vlines(p_bal, 0, y_end, colors='black', linestyles='solid', label='$p_{bal}$')
    plt.vlines(p_low, 0, y_end, colors='yellow', label='$p_{low}$')
    plt.grid()
    plt.xlim(0, x_end)
    plt.ylim(0, y_end)
    plt.xlabel('Price')
    plt.ylabel('Revenue')
    plt.legend()
    plt.title("Large Market Limits Revenue under Static and Dynamic Pricing: \n E[$\\Pi$(p)] vs. p, $\\gamma$=0")
    plt.savefig("Dynamic/Dynamic_Theoretic_Revenue")
    plt.show()


### Dynamic large market limit | Agent
def plotDynamicAgentLambda(df_result, p_max):
    plt.plot(df_result.index, df_result['Driver arrival rate | Agent'], color='red', label="$\\lambda_{agent}$")
    plt.plot(df_result.index, df_result['Driver arrival rate | Theoretic'], color='green', linestyle='dashed',
             label="$\\lambda_{theoretic}$")
    plt.grid()
    plt.xlim(0, p_max)
    plt.ylim(0, 1.4)
    plt.xlabel('Price', fontsize=12)
    plt.ylabel('$\\lim_{n\\to\\infty} \\lambda$(n,p)', fontsize=12)
    plt.legend()
    plt.title("Dynamic Large Market Limit | Agent: \n""$\\lambda$(n,p) vs. p")
    plt.savefig("Dynamic/Dynamic_Agent_Lambda")
    plt.show()


def plotDynamicAgentRevenue(df_result, p_max):
    plt.plot(df_result.index, df_result['Revenue | Agent'], color='red', label="$Revenue_{agent}$")
    plt.plot(df_result.index, df_result['Revenue | Theoretic'], color='green', linestyle='dashed',
             label="$Revenue_{theoretic}$")
    plt.grid()
    plt.xlim(0, p_max)
    plt.ylim(0, 3.5)
    plt.xlabel('Price')
    plt.ylabel('Revenue')
    plt.legend()
    plt.title("Dynamic Large Market Limit | Agent: \n E[$\\Pi$(p)] vs. p, $\\gamma$=0")
    plt.savefig("Dynamic/Dynamic_Agent_Revenue")
    plt.show()
