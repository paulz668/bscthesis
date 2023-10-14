import numpy as np
import os
from labelgen import *

cwd = os.getcwd()

for root, dirs, files in os.walk(cwd):
    for name in files:
        print(os.path.join(root, name))