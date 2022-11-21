@echo off

ECHO Submitting the job to AI platform..
:: Temporarily set an environment variable
SET TIER=BASIC
SET MODEL_NAME=sample_model_tf
SET MODEL_DIR=gs://%BUCKET_NAME%/%MODEL_NAME%

SET CurrDir=%CD%
CD..
SET PACKAGE_PATH=%CD%/SampleTrainer
CD %CurrDir%

:: Make bucket using gcloud's utilities
:: gsutil mb gs://%BUCKET_NAME%

:: get locale date via %date%, time via %time%
:: get part of date via %date:~start_pos,num_chars_from_pos%,
:: eg: %date:~0,2% to get the day
SET day=%date:~0,2%
SET month=%date:~3,3%
SET year=%date:~7,2%
SET hours=%time:~0,2%
SET mins=%time:~3,2%

SET EPOCH_FORMAT="%day%%month%_%hours%%mins%"
SET JOB_NAME="train_%MODEL_NAME%_%EPOCH_FORMAT%"

:: To Train sklearn estimator instead, use `--module-name=SampleTrainer.train_sklearn_cloud` instead
gcloud ai-platform jobs submit training %JOB_NAME% ^
    --job-dir=%MODEL_DIR% ^
    --runtime-version=%RUNTIME_VERSION% ^
    --region=%REGION% ^
    --scale-tier=%TIER% ^
    --package-path=%PACKAGE_PATH% ^
    --module-name=SampleTrainer.train_tf_cloud ^
    --python-version=%PYTHON_VERSION% ^
    --stream-logs ^
    -- ^
        -l %MODEL_DIR%

:: Remove a temporarily set variable
SET TIER=
SET MODEL_NAME=
SET MODEL_DIR=
SET CurrDir=
SET PACKAGE_PATH=
SET day=
SET month=
SET year=
SET hours=
SET mins=
SET EPOCH_FORMAT=
SET JOB_NAME=