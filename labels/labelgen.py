import numpy as np
import math

def ew(mp, a = 34.65620375):
    """
    calculate exponentially decaying weights based on array size of midprices
    de Prado (2017) suggests defining decay using a span of 100 which is equivalent to 34.65620375 when 
    defining decay in terms of halflife
    """
    return 1 + np.exp((-np.log(2) / a) * np.linspace(1, mp.size, mp.size, endpoint = True))

def wsd(mp, w):
    """
    calculate the weighted standard deviation based on an arrray of mid prices mp and an array
    of weights w
    """
    avg = np.average(mp, weights=w)
    var = np.average((mp-avg)**2, weights=w)
    return math.sqrt(var)

def ewmsd(mp, n, a = 34.65620375):
    """
    calculate exponentially weighted rolling standard deviation with sampling frequency n 
    """
    w = ew(mp, a)
    ewmsd = np.empty(mp.size)
    for i in range(mp.size):
        ewmsd[i] = wsd(mp[:i+1][::-n], w[:int(np.ceil((i+1)/n))][::-1])
    return ewmsd

def stbl(mp, ewmsd):
    """
    label observation at time t based on the static triple barrier method
    mp is an array like container of midprices from time t to t+n
    ewmsd is the exponentially weighted moving standard deviation at time t for sampling frequency n 
    1 signifies an up move, 2 a stationary move and 3 a down move
    """
    for i in range(mp.size):
        if i == 0:
            continue
        if mp[i] > (mp[0] + ewmsd):
            return 1
        elif mp[i] < (mp[0] - ewmsd):
            return 3
    return 2

def dtbl(mp, ewmsd):
    """
    label observation at time t based on the dynamic triple barrier method
    mp is an array like container of midprices from time t to t+n (length n+1)
    ewmsd is an array like container of exponentially weighted moving standard deviation at time t
    for the sampling frequencies from 1 to n (length n)
    n is the number periods the forecast looks into the future
    1 signifies an up move, 2 a stationary move and 3 a down move
    """
    for i in range(len(mp)):
        if i == 0:
            continue
        if mp[i] > (mp[0] + ewmsd[i-1]):
            return 1
        elif mp[i] < (mp[0] - ewmsd[i-1]):
            return 3
    return 2
