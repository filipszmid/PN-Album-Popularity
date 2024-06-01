#  type: ignore
# pylint: disable-all
"""Loading model"""
import os
import pickle

from popularity_forecaster.core.constants import PATH_TO_SCORES
from dotenv import load_dotenv
from loguru import logger
from popularity_forecaster.core.utils import fix_paths, get_current_model_patch, get_version, load_data, summary


class EvaluateModelWorkflow:
    def __init__(self):
        fix_paths()
        load_dotenv()
        self.MAX_R2 = float(os.environ["MAX_R2"])
        self.x_train, self.x_test, self.y_train, self.y_test = load_data()
        self.filename = get_current_model_patch()

    def load_model_from_disk(self):
        loaded_model = pickle.load(open(self.filename, "rb"))
        return loaded_model

    def evaluate_model(self, model):
        score = summary(model, self.x_train, self.y_train, self.x_test, self.y_test)
        if score > self.MAX_R2:
            logger.warning(
                "Model version " + get_version() + f" have greater R^2 than {0.3} "
            )
        return score

    @staticmethod
    def export_score(score):
        f = open(PATH_TO_SCORES + "score-v" + get_version() + ".txt", "w")
        f.write("{}".format(score))
        f.close()


if __name__ == "__main__":
    workflow = EvaluateModelWorkflow()
    model = workflow.load_model_from_disk()
    r2 = workflow.evaluate_model(model)
    workflow.export_score(r2)
