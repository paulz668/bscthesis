import numpy as np
import math

def ew(mpr, a = 34.65620375):
    """
    calculate exponentially decaying weights based on array size of midprice returns
    de Prado (2018) suggests defining decay using a span of 100 which is equivalent to a halflife of 34.65620375 
    when defining decay in terms of halflife
    """
    return 1 + np.exp((-np.log(2) / a) * np.linspace(1, mpr.size, mpr.size, endpoint = True))

def wsd(mpr, w):
    """
    calculate the weighted standard deviation based on an arrray of midprice returns mp and an array
    of weights w
    """
    avg = np.average(mpr, weights=w)
    var = np.average((mpr-avg)**2, weights=w)
    return math.sqrt(var)

def ewmsd(mpr, n, a = 34.65620375):
    """
    calculate exponentially weighted rolling standard deviation of mpr with sampling frequency n 
    """
    w = ew(mpr, a)
    ewmsd = np.empty(mpr.size)
    for i in range(mpr.size):
        ewmsd[i] = wsd(mpr[:i+1][::-n], w[:int(np.ceil((i+1)/n))][::-1])
    return ewmsd

def stbl(mpr, ewmsd):
    """
    label observation at time t based on the static triple barrier method
    mpr is an array like container of midprice returns from time t to t+n
    ewmsd is the exponentially weighted moving standard deviation at time t for sampling frequency n 
    1 signifies an up move, 2 a stationary move and 3 a down move
    """
    for i in range(mpr.size):
        if i == 0:
            continue
        if mpr[i] > (mpr[0] + ewmsd):
            return 1
        elif mpr[i] < (mpr[0] - ewmsd):
            return 3
    return 2

def dtbl(mpr, ewmsd):
    """
    label observation at time t based on the dynamic triple barrier method
    mpr is an array like container of midprice returns from time t to t+n (length n+1)
    ewmsd is an array like container of exponentially weighted moving standard deviation at time t
    for the sampling frequencies from 1 to n (length n)
    n is the number periods the forecast looks into the future
    1 signifies an up move, 2 a stationary move and 3 a down move
    """
    for i in range(mpr.size):
        if i == 0:
            continue
        if mpr[i] > (mpr[0] + ewmsd[i-1]):
            return 1
        elif mpr[i] < (mpr[0] - ewmsd[i-1]):
            return 3
    return 2