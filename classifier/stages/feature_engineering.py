#  type: ignore
# pylint: disable-all
"""Feature engineering"""

import os

import numpy as np
import pandas as pd
from constants import PATH_TO_BUCKET
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from utils import fix_paths


class FeatureEngineeringWorkflow:
    def __init__(self):
        load_dotenv()
        fix_paths()
        self.test_size = float(os.environ["TEST_SIZE"])
        self.df = pd.read_csv(
            "../data/bucket/preprocessed-pitchfork.csv", index_col=[0]
        )

    def generate_hot_encoded(self):
        hot_encoded = pd.get_dummies(self.df.genre)
        hot_encoded.columns = list(map(lambda x: f"{x}_onehot", hot_encoded.columns))
        hot_encoded.head()
        self.df = self.df.join(hot_encoded)
        self.features = [
            "releaseyear",
            "key",
            "acousticness",
            "danceability",
            "energy",
            "instrumentalness",
            "liveness",
            "loudness",
            "speechiness",
            "valence",
            "tempo",
        ] + list(hot_encoded.columns)

    def generate_train_test_sets(self) -> tuple:
        x = self.df[self.features].values
        y = self.df["score"].values
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=self.test_size, random_state=123
        )
        return x_train, x_test, y_train, y_test

    def save_train_test_sets(self, x_train, x_test, y_train, y_test) -> None:
        np.savetxt(PATH_TO_BUCKET + "x_train.csv", x_train, delimiter=",")
        np.savetxt(PATH_TO_BUCKET + "x_test.csv", x_test, delimiter=",")
        np.savetxt(PATH_TO_BUCKET + "y_train.csv", y_train, delimiter=",")
        np.savetxt(PATH_TO_BUCKET + "y_test.csv", y_test, delimiter=",")


if __name__ == "__main__":
    workflow = FeatureEngineeringWorkflow()
    workflow.generate_hot_encoded()
    x_train, x_test, y_train, y_test = workflow.generate_train_test_sets()
    workflow.save_train_test_sets(x_train, x_test, y_train, y_test)
