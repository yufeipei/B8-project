import matplotlib.pyplot as plt
import h5py
import itertools
import numpy as np
from PIL import Image
from scipy.stats import logistic
from scipy.stats import chi2
from scipy.stats import poisson
from scipy.stats import mode
from scipy.optimize import curve_fit
from scipy.optimize import least_squares
from scipy.optimize import leastsq
import math
from copy import deepcopy
from statistics import mean
import time
import csv
from scipy.optimize import fsolve

Pi = np.pi
Sqrt2 = np.sqrt(2)

Erf = []
for i in range(10**6 + 1):
    Erf.append(math.erf(i / 10**5))
for i in range(-10**6 , 0):
    Erf.append(math.erf(i / 10**5))