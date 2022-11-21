import os
import argparse
import logging
import gcsfs


from tempfile import TemporaryDirectory
from SampleTrainer import get_data, save_file
from pathlib import Path
import joblib
from sklearn.linear_model import LogisticRegression


def train(save_location, verbose):
    if verbose:
        print("Given location is: ", os.path.join("gs://", save_location))

    X, y = get_data(train=True)
    model = LogisticRegression(
        max_iter=200,
        n_jobs=-1,
    )

    model.fit(X, y)
    logging.info("[LOGGED]Estimator has been fitted.")

    with TemporaryDirectory() as tmp_dir:
        temp_save_location = Path(tmp_dir) / "model.joblib"
        joblib.dump(model, temp_save_location)

        save_file(temp_save_location, os.path.join("gs://", f"{save_location}.joblib"))

    if verbose:
        print("Done saving the model in: ", str(save_location))


if __name__ == "__main__":
    logging.basicConfig()
    logging.info("[LOGGED]Starting parsing arguments")

    parser = argparse.ArgumentParser(
        description="Train Simple NN on dummy data using sklearn"
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
    train(save_location, int(args.verbose))
