import pandas as pd
import numpy as np
import os
import json
from labelgen import *

def convert_numpy_integers(obj):
    if isinstance(obj, np.int64):
        return int(obj)
    elif isinstance(obj, list):
        return [convert_numpy_integers(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_numpy_integers(value) for key, value in obj.items()}
    else:
        return obj

# Create your dictionary with NumPy int64 values
labels = {
    "slmt1": {'1': [np.int64(0), np.int64(0), np.int64(0)], '2': [np.int64(0), np.int64(0), np.int64(0)], '3': [np.int64(0), np.int64(0), np.int64(0)], '5': [np.int64(0), np.int64(0), np.int64(0)], '10': [np.int64(0), np.int64(0), np.int64(0)]},
    # ... (other entries)
}

# Convert NumPy int64 values to regular Python integers
labels = convert_numpy_integers(labels)

with open('labels.json', 'w') as json_file:
    json.dump(labels, json_file, indent=4)