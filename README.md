# Sample Repo to train on GCP's AI-Platform

This is a small yet self-sufficient repo that can assist a new GCP user to train their tensorflow / sklearn model
and save it inside the assigned bucket.

## Introduction

AI-Platform is a prequel to their new [Vertex AI](https://cloud.google.com/vertex-ai) platform that supports python version upto 3.7. This repository
is mainly created to showcase how to train their model and hence is kept simple - dataset is two-class synthetic
data from `sklearn.datasets.make_classification()`. The package `SampleTrainer` contains code for both sklearn's
`LogisticRegression()` and tensorflow's 3-layer FCNN.

Since this is technically a package, it also needs `setuptools` to build it and the exact dependencies 
are mentioned in `setup.py`. To further simplify running this repo, I've also included shell scripts 
(`.cmd` for Windows user and `.sh` for Linux/Mac users) which makes to-and-fro calls to AI-Platform and hence can
be even run by a tech-savy non-coder.

A guide is also present inside [setup](/setup) directory that will help a new user setup their environment to run this code.
Do not forget to change the names as per your preferences / requirements.

## Directories Present
They are divided into two parts - directories which are read and committed via git and those that are excluded:
1. Excluded Directories: Apart from all the cache / packaging directories, there are two directories that 
I specifically chose to ignore:
    - `models/`: This directory will be created when either of the local versions of trainer are executed. sklearn
estimators are saved as a `.joblib` object whereas tensorflow creates a [directory](https://www.tensorflow.org/guide/saved_model).
    - `secrets/`: This directory will be unique to every user and contains a `json` file that is used for authentication
before a job is accepted for training. Make sure that no third party has access to contents in this directory.

2. Included Directories: Directories that are directly involved in training the model either locally or on cloud:
    - `SampleTrainer/`: This is the package that contains all the relevant python code to run the trainer.
    - `scripts/`: This directory contains shell scripts to push your package onto cloud, making a job and communicating
the logs back into your console without needing to visit GCP console.
    - `setup/`: The first directory that one should visit to understand how to correctly setup their environment - 
this involves creating a virtual python environment, setting up `gcloud` & service-account associated to this project
and giving appropriate access and permission to run it smoothly.

## Files Present
For this section, I've taken a breath-first search approach to list out every file, and it's usage in brief.
1. Top Level files:
   - `.gitignore`: This special file provides git with information about what kind of files should git ignore 
while managing others. These files are essentially out of version control.
   - `README.md`: This file, provides info about the entire repo.
   - `requirements.txt`: Normally used to mention all the dependencies that are to be installed in a python environment.
Many now prefer [other](https://godatadriven.com/blog/a-practical-guide-to-setuptools-and-pyproject-toml/) ways to do 
this. Visit this [link](https://caremad.io/posts/2013/07/setup-vs-requirement/) to check out what I've done.
   - `setup.py`: Set up the python package and contains dependencies via `setuptools`.
2. Inside `SampleTrainer`:
   - `__init__`: The file first read when this package is imported, contains access to direct utility functions.
   - `train_sklearn_cloud.py`, `train_sklearn_local.py`, `train_tf_cloud.py`, `train_tf_local.py` contains code to
perform the mentioned task.
     - `utils.py`: Contains utility functions that are to be used by other files.
3. Inside `scripts`:
   - `train_on_cloud.cmd` / `train_on_cloud.sh`: shell scripts for windows and linux respectively to directly 
connect to AI-Platform to run the job.
4. Inside `setup`:
   - `README.md`: Contains info on how to setup environment for running.
   - `set_variables.cmd` / `set_variables.sh`: Contains shell scripts to create some important environment variables.

## Conclusion
After successfully running the jobs, one would find their models in the bucket and AI-Platform console to have success
logs against that run. While useful to run archaic builds (python 3.7 and below), I find that Vertex-AI provides more
things than what AI-Platform does, it is also much simpler. 
So [migrating](https://cloud.google.com/vertex-ai/docs/start/migrating-to-vertex-ai) from AI-Platform 
or starting a new project in Vertex-AI will feel easier after going through this repo's content.
