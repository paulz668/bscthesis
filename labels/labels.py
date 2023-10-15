import numpy as np
import os
from labelgen import *

cwd = "YOUR PATH" # enter current work directory
n = [1,2,3,4,5,6,7,8,9,10] # sampling frequencies

for root, dirs, files in os.walk(cwd):
    for name in files:
        data = np.loadtxt(os.path.join(root, name).replace("\\", "/")) # load data
        mpr = np.diff(data[50, :], prepend=data[50, 0]) / data[50, :] # calculate simple returns for midprices
        mprsd = np.empty((10, mpr.size))
        for i in range(len(n)):
            mprsd[i,:] = ewmsd(mpr, n[i])
        print("EWMSD calculated")
        labels = np.empty((10, mpr.size))
        for i in range(mpr.size):
            # static tripple barrier labels
            labels[0, i] = stbl(mpr[i:i+2], mprsd[0, i])
            labels[1, i] = stbl(mpr[i:i+3], mprsd[1, i])
            labels[2, i] = stbl(mpr[i:i+4], mprsd[2, i])
            labels[3, i] = stbl(mpr[i:i+6], mprsd[4, i])
            labels[4, i] = stbl(mpr[i:i+11], mprsd[9, i])

            # dynamic triple barrier labels
            labels[5, i] = stbl(mpr[i:i+2], mprsd[0, i]) 
            # static and dynamic triple barrier are the same when the forcasting period is 1
            labels[6, i] = dtbl(mpr[i:i+3], mprsd[:2, i])
            labels[7, i] = dtbl(mpr[i:i+4], mprsd[:3, i])
            labels[8, i] = dtbl(mpr[i:i+6], mprsd[:5, i])
            labels[5, i] = dtbl(mpr[i:i+11], mprsd[:, i])
        np.savetxt('NL_' + name, np.vstack((data, labels)))
        print(name + " done")