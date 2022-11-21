import os
import logging

from tempfile import TemporaryDirectory
from SampleTrainer import get_data, parse, save_file
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
    save_location, verbosity = parse(type_of_model="sklearn")
    train(save_location, verbosity)
