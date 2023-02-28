#  type: ignore
# pylint: disable-all
"""Model training"""

import pickle

from sklearn.linear_model import LinearRegression

from utils import fix_paths, get_current_model_patch, load_data

fix_paths()

x_train, x_test, y_train, y_test = load_data()

reg = LinearRegression().fit(x_train, y_train)

filename = get_current_model_patch()
pickle.dump(reg, open(filename, "wb"))
