import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

df = pd.read_csv("../data/bucket/preprocessed-pitchfork.csv", index_col=[0])

hot_encoded = pd.get_dummies(df.genre)
hot_encoded.columns = list(map(lambda x: f"{x}_onehot", hot_encoded.columns))

hot_encoded.head()

df = df.join(hot_encoded)
print(df)

features = ["releaseyear", "key", "acousticness", "danceability",
                     "energy", "instrumentalness", "liveness", "loudness",
                     "speechiness", "valence", "tempo"] + list(hot_encoded.columns)
print(features)
x = df[features].values
y = df["score"].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state=123)

print(x_train)
print(type(x_train))

np.savetxt('../data/bucket/x_train.csv', x_train, delimiter=",")
np.savetxt('../data/bucket/x_test.csv', x_test, delimiter=",")
np.savetxt('../data/bucket/y_train.csv', y_train, delimiter=",")
np.savetxt('../data/bucket/y_test.csv', y_test, delimiter=",")