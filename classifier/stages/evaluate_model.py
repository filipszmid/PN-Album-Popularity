#  type: ignore
# pylint: disable-all
"""Loading model"""
import os
import pickle

from classifier.stages.constants import PATH_TO_SCORES
from utils import fix_paths, summary, get_current_model_patch, load_data, get_version
from loguru import logger
from dotenv import load_dotenv

fix_paths()
load_dotenv()
MAX_R2 = float(os.environ["MAX_R2"])


x_train, x_test, y_train, y_test = load_data()

# load the model from disk
filename = get_current_model_patch()
loaded_model = pickle.load(open(filename, "rb"))

r2 = summary(loaded_model, x_train, y_train, x_test, y_test)
if r2 > MAX_R2:
    logger.warning("Model version " + get_version() + f" have greater R^2 than {0.3} ")

f = open(PATH_TO_SCORES + "score-v" + get_version() + ".txt", "w")
f.write("{}".format(r2))
f.close()
