import os
import logging

import tensorflow as tf

from pathlib import Path
from tempfile import TemporaryDirectory
from SampleTrainer import get_data, parse


def train(save_location, verbose):
    if verbose:
        print("Given location is: ", save_location)

    X, y = get_data(train=True)
    keras_model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(X.shape[1], )),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(4, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])

    logging.info("[LOGGED]Model has been built.")
    if verbose:
        print(keras_model.summary())

    keras_model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics="accuracy",
    )

    logging.info("[LOGGED]Model has been compiled.")

    keras_model.fit(X, y, epochs=3, verbose=verbose)
    logging.info("[LOGGED]Model has been fitted.")

    with TemporaryDirectory() as tmp_dir:
        temp_save_loc = Path(tmp_dir) / "tf/"
        keras_model.save(str(temp_save_loc))

        for element in temp_save_loc.iterdir():
            if element.is_dir():
                file = os.path.join(f"gs://{save_location}", element.name)
                tf.io.gfile.makedirs(str(file))

        for dir, sub_dir, files in tf.io.gfile.walk(temp_save_loc):
            for file in files:
                file_loc = Path(dir) / file
                parent_dir = file_loc.parents[0]
                if parent_dir.name != "tf":
                    # change storage location if not the root directory
                    file = parent_dir.relative_to(file_loc.parents[1]) / str(file)
                tf.io.gfile.copy(str(file_loc), os.path.join(f"gs://{save_location}", str(file)))


if __name__ == "__main__":
    save_location, verbosity = parse(type_of_model="tf")
    train(save_location, verbosity)
