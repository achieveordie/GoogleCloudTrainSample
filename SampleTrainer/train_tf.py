import argparse

import tensorflow as tf

from pathlib import Path
from tempfile import TemporaryDirectory
from utils import get_data, save_file

RANDOM_STATE=10
SAVE_LOCATION = Path().cwd().parents[0] / "models/tf/"
SAVE_LOCATION.mkdir(exist_ok=False, parents=True)


def train(save_location, verbose):
    if verbose:
        print("Given location is: ", save_location)

    X, y = get_data(train=True)
    keras_model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(X.shape[1], )),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(4, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])

    if verbose:
        print(keras_model.summary())

    keras_model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics="accuracy",
    )

    keras_model.fit(X, y, epochs=3, verbose=verbose)
    # keras_model.save(save_location / "keras_model/")    # !Temporary!
    with TemporaryDirectory() as tmp_dir:
        temp_save_loc = Path(tmp_dir) / "tf/"
        keras_model.save(temp_save_loc)

        for element in temp_save_loc.iterdir():
            if element.is_dir():
                file = save_location / element.name
                file.mkdir()

        for dir, sub_dir, files in tf.io.gfile.walk(temp_save_loc):
            for file in files:
                file_loc = Path(dir) / file
                parent_dir = file_loc.parents[0]
                if parent_dir.name != "tf":
                    # change storage location if not the root directory
                    file = parent_dir.relative_to(file_loc.parents[1]) / file
                tf.io.gfile.copy(file_loc, save_location / file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train Simple NN on dummy data"
    )

    parser.add_argument(
        "-l",
        "--location",
        default=SAVE_LOCATION,
        help="The location to store the trained model",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        choices=["0", "1", "2"],
        default=0,
        help="Verbosity, choose between {0, 1, 2}",
    )

    args = parser.parse_args()
    train(args.location, int(args.verbose))
