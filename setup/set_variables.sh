#!/usr/bin/env bash
# Adapted from ai-plotform-samples's setup
# the link is: https://github.com/GoogleCloudPlatform/ai-platform-samples/blob/main/setup/variables.sh

function err() {
  echo "ERROR: $*" >&2
  return 1
}

function export_variables(){
  echoResults=false

  export RUNTIME_VERSION=2.1
  export PYTHON_VERSION=3.7
  export REGION=us-east1
  export SA_NAME=sagar-mishra
  export PROJECT_ID=geometric-petal-362311
  export BUCKET_NAME=model-storage-sample
  export GOOGLE_APPLICATION_CREDENTIALS=secrets/key.json

  if [ "${echoResults}" ]
  then
    echo "RUNTIME_VERSION=${RUNTIME_VERSION}"
    echo "PYTHON_VERSION=${PYTHON_VERSION}"
    echo "REGION=${REGION}"
    echo "SA_NAME=${SA_NAME}"
    echo "PROJECT_ID=${PROJECT_ID}"
  fi
}

main(){
  export_variables || err "Unable to set variables"
}

main "$@"