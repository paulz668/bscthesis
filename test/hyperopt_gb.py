import pandas as pd
import numpy as np
import os
import time
import json
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn import metrics
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
    
cwd = "C:/Users/paulz/Documents/UNI/BBE/7.Semester/Bachelorarbeit/LOB_DATA/1.NoAuction_Zscore/"

# Get list of names and sort them by day
names = os.listdir(cwd)
keys = lambda x: int(x[x.find('_', 21) + 1:].strip('.csv')) 
names.sort(key=keys)

list_df = [pd.read_csv(cwd + x, header=None) for x in names]

print('Data has been read')

# Define the objective function to be minimised
def objective_gb(hyperparameters):

    # Initialise Variables 
    start = 0
    end = 3
    counter = 0
    f1 = 0

    while end < len(names):

        # Define Training and Test Set
        training_df = pd.concat(list_df[start:end], ignore_index=True)
        X_train = training_df.iloc[:, :144]
        Y_train = training_df.iloc[:, 144]
        
        test_df = list_df[end]
        X_test = test_df.iloc[:, :144]
        Y_test = test_df.iloc[:, 144]

        # Fit model with input hyperparameters
        gb = HistGradientBoostingClassifier(**hyperparameters).fit(X_train, Y_train)

        # Predict Y
        Y_pred = gb.predict(X_test)

        # Calculate F1 score
        f1 += metrics.f1_score(Y_test, Y_pred, labels=[1.0, 2.0, 3.0], average='macro')

        # Increment Variables
        start += 1
        end += 1
        counter += 1
    
    # Divide sum of F1 scores by loops
    f1 /= counter

    return {
        'loss': f1,
        'status': STATUS_OK,
        'eval_time': time.time()
        }

space = {
    'learning_rate': hp.choice('learning_rate', list(np.linspace(0.01, 0.3, 30))),
    'max_iter': hp.choice('max_iter', [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]),
    'l2_regularization': hp.uniform('l2_regularization', 0.0, 5.0),
}

print('Parameter space has been defined')

trials = Trials()
best = fmin(objective_gb,
            space=space,
            algo=tpe.suggest,
            max_evals=100,
            trials=trials)

results = {
    'results': trials.trials
}

with open("hyperopt_gb_zscore.json", "w") as outfile:
    json.dump(results, outfile)