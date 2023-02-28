#  type: ignore
# pylint: disable-all
"""Loading model"""
import pickle

from classifier.stages.constants import PATH_TO_SCORES
from utils import fix_paths, summary, get_current_model_patch, load_data, get_version
from loguru import logger

fix_paths()

x_train, x_test, y_train, y_test = load_data()

# load the model from disk
filename = get_current_model_patch()
loaded_model = pickle.load(open(filename, "rb"))

r2 = summary(loaded_model, x_train, y_train, x_test, y_test)
logger.info("Model version " + get_version() + f" have R^2= {r2} ")

f = open(PATH_TO_SCORES + "model-v" + get_version() + ".txt", "w")
f.write("{}".format(r2))
f.close()