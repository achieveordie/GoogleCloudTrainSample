import gcsfs
import logging
import argparse

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


def parse(type_of_model):
    if type_of_model.lower() == "sklearn":
        description = "Train Simple NN estimator using sklearn"
    elif type_of_model.lower() == "tf":
        description = "Train simple NN model using tensorflow"
    else:
        raise ValueError(
                         f"Only expecting between `sklearn` and `tf`, "
                         f"found {type_of_model.lower()} instead."
        )

    logging.basicConfig()
    logging.info("[LOGGED]Starting parsing arguments")

    parser = argparse.ArgumentParser(
        description=description
    )

    parser.add_argument(
        "-l",
        "--location",
        help="The location to store the trained estimator",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        choices=["0", "1", "2"],
        default=0,
        help="Verbosity, choose between {0, 1, 2}",
    )

    parser.add_argument(
        "-j",
        "--job-dir",
        help="Argument passed by AI-Platform, not used here.",
    )

    args = parser.parse_args()
    if isinstance(args.location, str) and args.location.startswith("gs://"):
        fs = gcsfs.GCSFileSystem(
            token="cloud",
        )

        save_location = args.location.split("gs://")[-1]
        if not fs.exists(save_location):
            fs.makedir(save_location)

    else:
        raise ValueError("Unsupported Value: ", args.location)

    logging.info(f"[LOGGED]Parsed Arguments: {args}")

    return args.location, int(args.verbose)
