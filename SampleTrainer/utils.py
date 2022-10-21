from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from tensorflow.io import gfile

RANDOM_STATE = 20
RANDOM_STATE_SPLIT = 25


def _get_data(n_samples=500):
    return make_classification(
        n_samples=n_samples,
        n_features=10,
        n_informative=3,
        random_state=RANDOM_STATE,
    )


def get_data(train=True):
    X, y = _get_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        train_size=0.9,
        random_state=RANDOM_STATE_SPLIT
    )

    if train:
        return X_train, y_train
    else:
        return X_test, y_test


def save_file(file_loc, save_location):
    with gfile.GFile(file_loc, "rb") as temp_file:
        with gfile.GFile(save_location, "wb") as file:
            file.write(temp_file.read())
