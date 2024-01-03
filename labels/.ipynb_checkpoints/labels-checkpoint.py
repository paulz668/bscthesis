import pandas as pd
import numpy as np
import os
import json
from labelgen import *

cwd = "C:/Users/paulz/Documents/UNI/BBE/7. Semester/Bachelorarbeit/LOB_DATA/3.NoAuction_DecPre" # enter current work directory
n = [1,2,3,4,5,6,7,8,9,10] # sampling frequencies
labels = {
    "slmt1": {'1':[0,0,0],'2':[0,0,0],'3':[0,0,0],'5':[0,0,0],'10':[0,0,0]},  #keep count of labels 1,2,3 using the static labelling method (t=.001) for periods 1,2,3,5,10
    "slmt2": {'1':[0,0,0],'2':[0,0,0],'3':[0,0,0],'5':[0,0,0],'10':[0,0,0]},  #keep count of labels 1,2,3 using the static labelling method (t=.002) for periods 1,2,3,5,10
    "slmt3": {'1':[0,0,0],'2':[0,0,0],'3':[0,0,0],'5':[0,0,0],'10':[0,0,0]},  #keep count of labels 1,2,3 using the static labelling method (t=.003) for periods 1,2,3,5,10
    "stbml": {'1':[0,0,0],'2':[0,0,0],'3':[0,0,0],'5':[0,0,0],'10':[0,0,0]},  #keep count of labels 1,2,3 using the static triple barrier labelling method for periods 1,2,3,5,10
    "dtbml": {'1':[0,0,0],'2':[0,0,0],'3':[0,0,0],'5':[0,0,0],'10':[0,0,0]}   #keep count of labels 1,2,3 using the dynamic triple barrier labelling method for periods 1,2,3,5,10
}
sampling_freq = [1,2,3,5,10]

for root, dirs, files in os.walk(cwd):
    for name in files:
        data = np.loadtxt(os.path.join(root, name).replace("\\", "/")) # load data
        df = pd.DataFrame(data[:144, :].T) # df of data without label
        mp = pd.DataFrame(data[42, :], columns=['Mid-price']) # df of mid-prices

        dlabel = pd.DataFrame(data[144:, :].T, columns=['1_t2', '2_t2', '3_t2', '5_t2', '10_t2']) # df of existing data labels
        for i in range(len(dlabel.columns)): # count label frequencies
            vals = dlabel.iloc[:,i].value_counts()
            labels["slmt2"][str(sampling_freq[i])][0] += vals[1]
            labels["slmt2"][str(sampling_freq[i])][1] += vals[2]
            labels["slmt2"][str(sampling_freq[i])][2] += vals[3]
        print("Default labels counted")

        pct = np.empty((mp.size, 5))
        for i in range(mp.size):
            for j in range(5):
                pct[i,j] = pct_change(mp[i:], sampling_freq[j])
        pct = pd.DataFrame(pct)
        print("pct_change calculations done")

        t1 = pct.map(lambda x: slm(x, t = 0.001))
        t1.columns = ['1_t1', '2_t1', '3_t1', '5__t1', '10_t1']
        t3 = pct.map(lambda x: slm(x, t = 0.003))
        t3.columns = ['1_t3', '2_t3', '3_t3', '5__t3', '10_t3']
        for i in range(len(t1.columns)): # count label frequencies
            vals = t1.iloc[:,i].value_counts()
            labels["slmt1"][str(sampling_freq[i])][0] += vals[1]
            labels["slmt1"][str(sampling_freq[i])][1] += vals[2]
            labels["slmt1"][str(sampling_freq[i])][2] += vals[3]

            vals = t3.iloc[:,i].value_counts()
            labels["slmt3"][str(sampling_freq[i])][0] += vals[1]
            labels["slmt3"][str(sampling_freq[i])][1] += vals[2]
            labels["slmt3"][str(sampling_freq[i])][2] += vals[3]
        print("t1 and t3 labels counted")

        ewmsd = pd.DataFrame()
        for i in range(10):
            name_df = ["ewmsd" + str(i)]  # name to merge series
            dfsd = pd.DataFrame(columns=name_df)
            for j in range(n[i]):
                temp_dfsd = mp[(mp.index-j) % n[i] == 0].ewm(span=100).std()
                temp_dfsd.columns = name_df
                temp_dfsd['original_index'] = temp_dfsd.index
                if dfsd.empty:
                    dfsd = temp_dfsd
                else:    
                    dfsd = pd.concat([dfsd, temp_dfsd])
            dfsd.sort_values('original_index', inplace=True)
            dfsd.drop('original_index', axis=1, inplace=True)
            if ewmsd.empty:
                ewmsd = dfsd
            else:
                ewmsd = pd.concat([ewmsd, dfsd], axis=1)
        ewmsd.replace(np.nan, 0, inplace=True)
        print("Ewmsd calculation done")

        stbmlabel = np.empty((mp.size, 5))
        dtbmlabel = np.empty((mp.size, 5))
        for i in range(mp.size):
            for j in range(5):
                stbmlabel[i,j] = stbml(mp.iloc[i:i+1+sampling_freq[j]], ewmsd.iloc[i,sampling_freq[j]-1])
                dtbmlabel[i,j] = dtbml(mp.iloc[i:i+1+sampling_freq[j]], ewmsd.iloc[i, :sampling_freq[j]])
        stbmlabel = pd.DataFrame(stbmlabel, columns=['1_stbml', '2_stbml', '3_stbml', '5_stbml', '10_stbml'])
        dtbmlabel = pd.DataFrame(dtbmlabel, columns=['1_dtbml', '2_dtbml', '3_dtbml', '5_dtbml', '10_dtbml'])
        print("Triple barrier labels calculated")

        for i in range(len(stbmlabel.columns)): # count label frequencies
            vals = stbmlabel.iloc[:,i].value_counts()
            labels["stbml"][str(sampling_freq[i])][0] += vals[1]
            labels["stbml"][str(sampling_freq[i])][1] += vals[2]
            labels["stbml"][str(sampling_freq[i])][2] += vals[3]

            vals = dtbmlabel.iloc[:,i].value_counts()
            labels["dtbml"][str(sampling_freq[i])][0] += vals[1]
            labels["dtbml"][str(sampling_freq[i])][1] += vals[2]
            labels["dtbml"][str(sampling_freq[i])][2] += vals[3]
        print("stbml and dtbml labels counted")   

        labeldf = t1.join(dlabel).join(t3).join(stbmlabel).join(dtbmlabel)
        name_list = [name[:-4] + "_labels" + ".csv", name[:-4] + "_features" + ".csv"]
        labeldf.to_csv(name_list[0])
        df.to_csv(name_list[1])
        print(name + ' features and labels downloaded')     

labels = convert_numpy_integers(labels)
with open('labels.json', 'w') as json_file:
    json.dump(labels, json_file, indent=4)