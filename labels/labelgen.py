import numpy as np
import pandas as pd

def EWMSD(df, n, span0 = 100):
    """
    calculate exponentially weighted rolling standard deviation with lookback period span0
    and sampling frequency n 
    """
    return None

def STBL(mp, ewmsd, n):
    """
    label observation at time t based on the static triple barrier method
    mp is an array like container of midprices from time t to t+n
    ewmsd is the exponentially weighted moving standard deviation at time t for sampling frequency n
    n is the number of periods the forecast looks into the future 
    1 signifies an up move, 2 a stationary move and 3 a down move
    """
    for i in range(len(mp)):
        if i == 0:
            continue
        if mp[i] > (mp[0] + ewmsd):
            return 1
        elif mp[i] < (mp[0] + ewmsd):
            return 3
    return 2

def DTBL(mp, ewmsd, n):
    """
    label observation at time t based on the dynamic triple barrier method
    mp is an array like container of midprices from time t to t+n
    ewmsd is an array like container of exponentially weighted moving standard deviation at time t
    for the sampling frequencies from 1 to n
    n is the number periods the forecast looks into the future
    1 signifies an up move, 2 a stationary move and 3 a down move
    """
    for i in range(len(mp)):
        if i == 0:
            continue
        if mp[i] > (mp[0] + ewmsd[i-1]):
            return 1
        elif mp[i] < (mp[0] +ewmsd[i-1]):
            return 3
    return 2
    