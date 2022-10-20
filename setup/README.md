This provides clear instructions on how to setup this project.

### Instructions
1. Create a new python environment with required version of python.
2. Ensure the Google SDK has been installed.
3. Run `gcloud init` to create default configuration, or if a different
   configuration file is required in case of a different project,
   run `gcloud config configurations --help` to understand how to set it up.
4. If you're on Windows-based system, look into `set_variables.cmd` and
   change the values of the environment variables as required, do it for
   `set_variables.sh` in case of UNIX-based systems.
5. RUN either of the above via `set_variables.cmd` OR `bash set_variables.sh`
   depending on the OS, after ensuring the current director is `setup`.
6. Check if the environments are set properly, this will be reset after closing
   the command line.
7. After coming back to the main directory, create a `gcloud` service account via command line via:

   `gcloud iam service-accounts create ${SA_NAME} --display-name="<Enter info>"`
8. Grant necessary roles for key creation:

   `gcloud projects add-iam-policy-binding ${PROJECT_ID} --member serviceAccount:${SA_NAME}@{PROJECT_ID}.iam.gserviceaccount.com --role roles/ml.developer`

   and

   `gcloud projects add-iam-policy-binding ${PROJECT_ID} --member serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com --role roles/storage.objectAdmin`

9. Download the service account key and store it in the env variable mentioned:
   `gcloud iam service-accounts keys create ${GOOGLE_APPLICATION_CREDENTIALS} --iam-account ${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com`

#### Notes:
- Use `%VARIABLE_NAME%` instead of `${VARIABLE_NAME}` in case of running above commands on Windows.