import pandas as pd
import math

def pct_change(mp, n):
    """
    Percentage Change (per Ntakaris et al. 2018)
    calculate the percentage of mp.iloc[0] to mp.iloc[n] with the method outlined in Benchmark 
    dataset for mid-price forecasting of limit order book data with machine learning methods
    """
    if n < mp.size:
        return (1/n*sum(mp.iloc[1:n+1]-mp.iloc[0]))/mp.iloc[0]
    return 0

def slm(pcmp, t = 0.002):
    """
    Static Labelling Method (per Ntakaris et al. 2018)
    calculate labels based on a threshold for the percentage change of t (default 0.002)
    for a percentage change equal to or greater than t, label 1 is used
    for a percentage change greater than −t and smaller than t, label 2 is used
    for percentage change smaller or equal to -t, label 3 is used
    pcmp is the percentage change of the mid-price from time t to t+n
    """
    if pcmp >= t:
        return 1
    elif pcmp <= -t:
        return 3
    return 2 


def stbml(mp, ewmsd):
    """
    Static Triple Barrier Method Label
    label observation at time t based on the static triple barrier method
    mp is a pd.Series of mid-prices from time t to t+n
    ewmsd is the exponentially weighted moving standard deviation at time t for sampling frequency n 
    1 signifies an up move, 2 a stationary move and 3 a down move
    """
    for i in range(mp.size):
        if i == 0:
            continue
        if mp.iloc[i] > (mp.iloc[0] + ewmsd):
            return 1
        elif mp.iloc[i] < (mp.iloc[0] - ewmsd):
            return 3
    return 2

def dtbml(mp, ewmsd):
    """
    Dynamic Triple Barrier Method Label
    label observation at time t based on the dynamic triple barrier method
    mp is a pd.Series of mid-prices from time t to t+n (length n+1)
    ewmsd is a pd.Series of exponentially weighted moving standard deviation at time t
    for the sampling frequencies from 1 to n (length n)
    n is the number periods the forecast looks into the future
    1 signifies an up move, 2 a stationary move and 3 a down move
    """
    for i in range(mp.size):
        if i == 0:
            continue
        if mp.iloc[i] > (mp.iloc[0] + ewmsd.iloc[i-1]):
            return 1
        elif mp.iloc[i] < (mp.iloc[0] - ewmsd.iloc[i-1]):
            return 3
    return 2