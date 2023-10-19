import numpy as np
import os
import json
from labelgen import *

cwd = "YOUR PATH" # enter current work directory
n = [1,2,3,4,5,6,7,8,9,10] # sampling frequencies
labels = {
    "slmt1": [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],  #keep count of labels 1,2,3 using the static labelling method (t=.001) for periods 1,2,3,5,10
    "slmt2": [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],  #keep count of labels 1,2,3 using the static labelling method (t=.002) for periods 1,2,3,5,10
    "slmt3": [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],  #keep count of labels 1,2,3 using the static labelling method (t=.003) for periods 1,2,3,5,10
    "stbml": [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],  #keep count of labels 1,2,3 using the static triple barrier labelling method for periods 1,2,3,5,10
    "dtbml": [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]   #keep count of labels 1,2,3 using the dynamic triple barrier labelling method for periods 1,2,3,5,10
}

for root, dirs, files in os.walk(cwd):
    for name in files:
        data = np.loadtxt(os.path.join(root, name).replace("\\", "/")) # load data
        df = pd.DataFrame(data[:145, :].T) # df of data without label
        mp = pd.DataFrame(data[50, :], columns='Mid-price') # df of mid-prices

        dlabel = pd.DataFrame(data[145:, :].T, columns=['t2_1', 't2_2', 't2_3', 't2_5', 't2_10']) # df of existing data labels
        for i in range(len(dlabel.columns)): # count label frequencies
            vals = dlabel.iloc[:,i].value_counts()
            labels["slmt2"][i][0] = vals[1]
            labels["slmt2"][i][1] = vals[2]
            labels["slmt2"][i][2] = vals[3]
        print("Default labels counted")

        pct = pd.DataFrame(columns=[1,2,3,5,10])
        for i in range(mp.size):
            pct.loc[len(pct.index)] = [pct_change(mp.iloc[i:], 1), pct_change(mp.iloc[i:], 2), pct_change(mp.iloc[i:], 3), 
                                      pct_change(mp.iloc[i:], 4), pct_change(mp.iloc[i:], 5)]
        print("pct_change calculations done")

        ewmsd = pd.DataFrame() 
        for i in range(10):
            name = ["ewmsd" + str(i)] # name to merge series 
            dfsd = pd.DataFrame(columns=name)
            for j in range(n[i]):
                temp_dfsd = mp[(mp.index-j) % n[i] == 0].ewm(span=100).std()
                temp_dfsd.columns = name
                dfsd.merge(temp_dfsd, how='outer')
            ewmsd[name] = dfsd
            print("Ewmsd for sampling period " + str(i) + " done")
        ewmsd.replace(np.nan, 0)
        print("Ewmsd calculation done")

        t1 = pct.map(slm, t = 0.001)
        t3 = pct.map(slm, t = 0.003)
        for i in range(len(t1.columns)): # count label frequencies
            vals = t1.iloc[:,i].value_counts()
            labels["slmt1"][i][0] = vals[1]
            labels["slmt1"][i][1] = vals[2]
            labels["slmt1"][i][2] = vals[3]

            vals = t3.iloc[:,i].value_counts()
            labels["slmt3"][i][0] = vals[1]
            labels["slmt3"][i][1] = vals[2]
            labels["slmt3"][i][2] = vals[3]
        print("t1 and t3 labels counted")
        

with open("label_freq.json", "w") as outfile:
    json.dump(labels)