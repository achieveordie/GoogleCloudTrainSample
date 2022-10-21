import argparse

import tensorflow as tf

from tempfile import TemporaryDirectory
from utils import get_data, save_file
from pathlib import Path
import joblib
from sklearn.linear_model import LogisticRegression

RANDOM_STATE = 10
SAVE_LOCATION = Path().cwd().parents[0] / "models/sklearn/"
SAVE_LOCATION.mkdir(exist_ok=True, parents=True)


def train(save_location):
    print("Given location is: ", save_location)
    save_location = Path(save_location) / "model.joblib"

    X, y = get_data(train=True)
    model = LogisticRegression(
        max_iter=200,
        n_jobs=-1
    )
    model.fit(X, y)
    with TemporaryDirectory() as tmp_dir:
        temp_save_loc = Path(tmp_dir) / "model.joblib"
        joblib.dump(model, temp_save_loc)

        save_file(temp_save_loc, save_location)

        with tf.io.gfile.GFile(temp_save_loc, "rb") as temp_file:
            with tf.io.gfile.GFile(save_location, "wb") as file:
                file.write(temp_file.read())

    print("Done Saving the model in: ", str(save_location))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train LogisticRegression on dummy data"
    )

    parser.add_argument(
        "-l",
        "--location",
        default=SAVE_LOCATION,
        help="The location to store the trained model",
    )
    args = parser.parse_args()
    train(args.location)
