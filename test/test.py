import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn import metrics
import os
import json

cwd = "C:/Users/paulz/Documents/UNI/BBE/7.Semester/Bachelorarbeit/LOB_DATA/1.NoAuction_Zscore/"

# Get list of names and sort them by day
names = os.listdir(cwd)
keys = lambda x: int(x[x.find('_', 21) + 1:].strip('.csv')) 
names.sort(key=keys)

list_df = [pd.read_csv(cwd + x, header=None) for x in names]

f1_gb = [0] * 9
accuracy_gb = [0] * 9
recall_gb = [0] * 9
precision_gb = [0] * 9

f1_rf = [0] * 9
accuracy_rf = [0] * 9
recall_rf = [0] * 9
precision_rf = [0] * 9

for i in range(1, 10):
    start = 0
    end = start + i
    counter = 0
    while end < len(names):
        training_df = pd.concat(list_df[start:end], ignore_index=True)
        X_train = training_df.iloc[:, :144]
        Y_train = training_df.iloc[:, 144]
        
        test_df = list_df[end]
        X_test = test_df.iloc[:, :144]
        Y_test = test_df.iloc[:, 144]

        gb = HistGradientBoostingClassifier().fit(X_train, Y_train)
        Y_pred_gb = gb.predict(X_test)
        f1_gb[i - 1] += metrics.f1_score(Y_test, Y_pred_gb, labels=[1.0, 2.0, 3.0], average='weighted')
        accuracy_gb[i - 1] += metrics.accuracy_score(Y_test, Y_pred_gb)
        recall_gb[i - 1] += metrics.recall_score(Y_test, Y_pred_gb, labels=[1.0, 2.0, 3.0], average='weighted')
        precision_gb[i - 1] += metrics.precision_score(Y_test, Y_pred_gb, labels=[1.0, 2.0, 3.0], average='weighted')

        rf = RandomForestClassifier().fit(X_train, Y_train)
        Y_pred_rf = rf.predict(X_test)
        f1_rf[i - 1] += metrics.f1_score(Y_test, Y_pred_rf, labels=[1.0, 2.0, 3.0], average='weighted')
        accuracy_rf[i - 1] += metrics.accuracy_score(Y_test, Y_pred_rf)
        recall_rf[i - 1] += metrics.recall_score(Y_test, Y_pred_rf, labels=[1.0, 2.0, 3.0], average='weighted')
        precision_rf[i - 1] += metrics.precision_score(Y_test, Y_pred_rf, labels=[1.0, 2.0, 3.0], average='weighted')

        start += 1
        end += 1
        counter += 1
    f1_gb[i - 1] /= counter
    accuracy_gb[i - 1] /= counter
    recall_gb[i - 1] /= counter
    precision_gb[i - 1] /= counter

    f1_rf[i - 1] /= counter
    accuracy_rf[i - 1] /= counter
    recall_rf[i - 1] /= counter
    precision_rf[i - 1] /= counter

    print(f'Round {i} done')

dict_metrics = {
    'gb': {
        'f1': f1_gb,
        'accuracy': accuracy_gb,
        'recall': recall_gb,
        'precision': precision_gb
    },
    'rf': {
        'f1': f1_rf,
        'accuracy': accuracy_rf,
        'recall': recall_rf,
        'precision': precision_rf
    }
}

with open("metrics.json", "w") as outfile:
    json.dump(dict_metrics, outfile)