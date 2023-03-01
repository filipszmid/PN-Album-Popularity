#  type: ignore
# pylint: disable-all
"""Model training"""

import pickle

from sklearn.linear_model import LinearRegression
from utils import fix_paths, get_current_model_patch, load_data


class TrainModelWorkflow:
    def __init__(self):
        fix_paths()
        self.x_train, self.x_test, self.y_train, self.y_test = load_data()
        self.model = LinearRegression()
        self.filename = get_current_model_patch()

    def fit_model(self):
        self.reg = self.model.fit(self.x_train, self.y_train)

    def save_model(self):
        pickle.dump(self.reg, open(self.filename, "wb"))


if __name__ == "__main__":
    workflow = TrainModelWorkflow()
    workflow.fit_model()
    workflow.save_model()
