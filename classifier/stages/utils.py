#  type: ignore
# pylint: disable-all
"""Utilities"""

import os

import numpy as np
from sklearn.metrics import mean_squared_error

from classifier.stages.constants import PATH_TO_BUCKET


def replace_genre(x):
    if not x or x == "none":
        return "Other"
    return x


def summary(model, x_train, y_train, x_test, y_test):
    """Prints regression model summary"""
    r2 = model.score(x_test, y_test)
    y_pred = model.predict(x_test)

    print(f"train size: {x_train.shape[0]} test size: {x_test.shape[0]}")
    print("Coefficients: \n", model.coef_)
    print(f"R^2: {r2}")
    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))

    return r2


def fix_paths():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


def get_version() -> str:
    f = open("../../VERSION", "r")
    return f.read()


def get_current_model_patch() -> str:
    return "../data/models/finalized_model-v" + get_version() + ".sav"


def load_data() -> tuple:
    x_train = np.loadtxt(PATH_TO_BUCKET + "x_train.csv", delimiter=",")
    x_test = np.loadtxt(PATH_TO_BUCKET + "x_test.csv", delimiter=",")
    y_train = np.loadtxt(PATH_TO_BUCKET + "y_train.csv", delimiter=",")
    y_test = np.loadtxt(PATH_TO_BUCKET + "y_test.csv", delimiter=",")
    return x_train, x_test, y_train, y_test
