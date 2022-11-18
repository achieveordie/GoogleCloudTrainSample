
set -v

TIER=BASIC

EXPORT MODEL_NAME=sample_model_tf
EXPORT MODEL_DIR=gs://"${BUCKET_NAME}"/"${MODEL_NAME}"

EXPORT PACKAGE_PATH=./SampleTrainer

EPOCH_FORMAT="${%d%m_%H%M}"
JOB_NAME=train_"${MODEL_NAME}"_"${EPOCH_FORMAT}"

gcloud ai-platform jobs submit training "${JOB_NAME}" \
    --job-dir="${MODEL_DIR}" \
    --runtime-version="${RUNTIME_VERSION}" \
    --region="${REGION}" \
    --scale-tier="${TIER}" \
    --package-path="${PACKAGE_PATH}" \
    --module-name=trainer.task \
    --python-version="${PYTHON_VERSION}" \
    --stream-logs \
    -- \
      "-l ${MODEL_DIR}"

set -
