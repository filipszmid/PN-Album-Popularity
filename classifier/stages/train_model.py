#  type: ignore
# pylint: disable-all
"""Model training"""

import pickle

import numpy as np
from sklearn.linear_model import LinearRegression

from constants import PATH_TO_BUCKET
from utils import fix_paths, summary

fix_paths()

x_train = np.loadtxt(PATH_TO_BUCKET+"x_train.csv", delimiter=",")
x_test = np.loadtxt(PATH_TO_BUCKET+"x_test.csv", delimiter=",")
y_train = np.loadtxt(PATH_TO_BUCKET+"y_train.csv", delimiter=",")
y_test = np.loadtxt(PATH_TO_BUCKET+"y_test.csv", delimiter=",")

reg = LinearRegression().fit(x_train, y_train)

r2 = summary(reg, x_train, y_train, x_test, y_test)
print(r2)

filename = "../data/bucket/finalized_model.sav"
pickle.dump(reg, open(filename, "wb"))

