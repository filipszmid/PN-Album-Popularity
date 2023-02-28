import os

from sklearn.metrics import euclidean_distances, r2_score, mean_squared_error

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