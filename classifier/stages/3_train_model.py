from sklearn.linear_model import LinearRegression
import numpy as np
import pickle
from classifier.stages import utils

x_train=np.loadtxt('../data/bucket/x_train.csv', delimiter=",")
x_test=np.loadtxt('../data/bucket/x_test.csv', delimiter=",")
y_train=np.loadtxt('../data/bucket/y_train.csv', delimiter=",")
y_test=np.loadtxt('../data/bucket/y_test.csv', delimiter=",")

reg = LinearRegression().fit(x_train, y_train)

r2 = utils.summary(reg, x_train, y_train, x_test, y_test)
print(r2)

filename = '../data/bucket/finalized_model.sav'
pickle.dump(reg, open(filename, 'wb'))

# some time later...
print("---------")
# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(x_test, y_test)
print(result)