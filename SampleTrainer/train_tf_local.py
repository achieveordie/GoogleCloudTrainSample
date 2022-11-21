import argparse
import logging

import tensorflow as tf

from pathlib import Path
from tempfile import TemporaryDirectory
from SampleTrainer import get_data

SAVE_LOCATION = Path.cwd().parents[0] / "models/tf/"
SAVE_LOCATION.mkdir(exist_ok=False, parents=True)


def train(save_location, verbose):
    logging.info("[Logged]Starting training, given save loc: ", save_location)
    if verbose:
        print("Given location is: ", save_location)

    X, y = get_data(train=True)
    keras_model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(X.shape[1], )),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(4, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])

    logging.info("[Logged]Model has been built.")
    if verbose:
        print(keras_model.summary())

    keras_model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics="accuracy",
    )

    logging.info("[Logged]Model has been compiled.")

    keras_model.fit(X, y, epochs=3, verbose=verbose)
    logging.info("Model has been fitted.")

    with TemporaryDirectory() as tmp_dir:
        temp_save_loc = Path(tmp_dir) / "tf/"
        keras_model.save(str(temp_save_loc))

        for element in temp_save_loc.iterdir():
            if element.is_dir():
                file = save_location / element.name
                tf.io.gfile.makedirs(str(file))

        for dir, sub_dir, files in tf.io.gfile.walk(temp_save_loc):
            for file in files:
                file_loc = Path(dir) / file
                parent_dir = file_loc.parents[0]
                if parent_dir.name != "tf":
                    # change storage location if not the root directory
                    file = parent_dir.relative_to(file_loc.parents[1]) / str(file)
                tf.io.gfile.copy(str(file_loc), str(save_location / str(file)))

    logging.info("[Logged]Model has been saved to the given location.")


if __name__ == "__main__":
    logging.basicConfig()
    logging.info("[Logged]Starting parsing arguments")

    parser = argparse.ArgumentParser(
        description="Locally train Simple NN on dummy data"
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
    logging.info(f"[Logged]Parsed arguments: {args}")

    train(args.location, int(args.verbose))
