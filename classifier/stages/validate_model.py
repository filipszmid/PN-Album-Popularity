#  type: ignore
# pylint: disable-all
"""Loading model"""
import pickle

import numpy as np

from constants import PATH_TO_BUCKET
from utils import fix_paths, summary

fix_paths()

x_train = np.loadtxt(PATH_TO_BUCKET+"x_train.csv", delimiter=",")
x_test = np.loadtxt(PATH_TO_BUCKET+"x_test.csv", delimiter=",")
y_train = np.loadtxt(PATH_TO_BUCKET+"y_train.csv", delimiter=",")
y_test = np.loadtxt(PATH_TO_BUCKET+"y_test.csv", delimiter=",")

# load the model from disk
filename = "../data/finalized_model.sav"
loaded_model = pickle.load(open(filename, "rb"))
result = loaded_model.score(x_test, y_test)
print(result)

r2 = summary(loaded_model, x_train, y_train, x_test, y_test)
print(r2)