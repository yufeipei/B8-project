"""

This file contains tabulars of values of certain types of functions e.g. erf that may be useful in the calculations.

"""

import matplotlib.pyplot as plt
import h5py
import itertools
import numpy as np
from PIL import Image
from scipy.stats import logistic
from scipy.stats import chi2
from scipy.stats import poisson
from scipy.stats import mode
import math
from copy import deepcopy
from statistics import mean
import time
import csv


Erf=[]
for i in range(1*10**6+1):
    Erf.append(math.erf(i/10**5))
for i in range(-1*10**6,0):
    Erf.append(math.erf(i/10**5))

# The value of Pi and sqrt(2) which are used frequently in the calculations.

Pi=3.14159265359
    
Sqrt2=1.414213562373

if __name__=="__main__":
    print(len(Erf))