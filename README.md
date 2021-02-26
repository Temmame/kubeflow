# DESCRIPTION
This folder contains the description of two different deployment methods : 
1. poc_aiplatform: 
* query data from bigquery
* train a model 
* saves outputs in GCS
* deploy the model 

2. poc_aiplatform_kubeflow: the same process but in this notebook we use a pipeline on kubeflow.

# BUILD `poc_aiplatform`



- Create a cluster from Kubeflow service on GCP, then scroll down and deploy it
- Create a notebook instance from *AI Platform -> Notebooks (Python3)*
- Launch the instance
- Upload the notebooks in the notebooks folder then open `poc_aiplatform` notebook
- Fill in the empty parameters about output bucket, model name, etc...
- Run cells

*Note : after the deployment is finished, you can see the model in `AI Platform --> Models` in the user interface*

# BUILD `poc_aiplatform_kubeflow`

#### LAUNCH INSTANCES : 

- Create a cluster from Kubeflow service on GCP
- Scroll down and deploy it
- Create a notebook instance from *AI Platform --> Notebooks (Python3)* 
- Launch instance
- Upload the notebooks (in the `notebooks` folder) then open `poc_aiplatform_kubeflow` notebook

#### LINK NOTEBOOK AND KUBEFLOW PIPELINE

- Go to *AI Platform --> Pipeline*
- Wait for the deployment of the cluster to be complete, when the notifications bell (on the top right) says Deployment is successful.
- Click on `Settings` at right of Pipeline 
- Copy the key
- Paste it in the `host=""` client's parameter in the launched notebook 
 

#### BUILD IMAGES FROM SHELL :

- Copy `ai-platform` folder in the cloud shell by uploading folder or click and drag in the shell's editor
- Change directory: `cd ai-platform`
- Make the shell script executable : `chmod +x ./env.sh`
- Execute the shell script : `./env.sh`

#### EDIT PARAMETERS AND RUN NOTEBOOK

- Go in the REGISTRY CONTAINER
- Copy every image (in the format `gcr.io/PROJECT_ID/image@sha*`) and paste it in the required field in the notebook :
    - IMG_PREPROCESS
    - IMG_TRAIN
    - IMG_TEST
- Fill in the empty parameters in the notebook about GCS bucket, model name, model version, etc...
- Run all the cells of the notebook : in the cell *run_pipeline*, wait for the pipeline to be completed

*Note : after the deployment is finished, you can see the model in `AI Platform --> Models` in the user interface*

# TEST DEPLOYED MODELS (for the two notebooks)

This section is valid for both notebooks.

From shell :
- `MODEL_NAME='<model_name>'`
- `MODEL_VERSION='<model_version>'`
- `PROJECT_ID='<project_id>'`
- `cd ai-platform`
- `gcloud config set account <xxxxx@gmail.com>`

There are two options, and a test file for each. Both are also launched from shell. You can use one of those two options :

1. `gcloud ai-platform predict --model=$MODEL_NAME --version=$MODEL_VERSION --json-instances=tests/test_gcloud.json`

2. 
- `ACCESS_TOKEN="$(gcloud auth application-default print-access-token)"`

- `curl -H "Content-Type: application/json" --data @tests/test_curl.json https://ml.googleapis.com/v1/projects/${PROJECT_ID}/models/${MODEL_NAME}/versions/${MODEL_VERSION}:predict\?access_token\=${ACCESS_TOKEN}`


# NOTES FOR KUBEFLOW

- The model must be saved with the name "model.pkl" to be deployed correctly, otherwise the deployment image won't work.

- In every python script, storing data in GCS is optional, except for the training step, specially if the model needs to be deployed from kubeflow

- For every step, you can use built-in images : like the download image (that queries data from Bigquery and store it in GCS) and the deploy image in the `poc_kubeflow` notebook, or you can build your own images, like the preprocess, train and test images. 

- Actually it's possible to use a python function as a step of a pipeline, without going through docker, but it must be in "standalone" format. See this section :
`https://www.kubeflow.org/docs/pipelines/sdk/python-function-components/`

- The output of every step of the pipeline needs to be an internal. For example, even though preprocess step saves data locally and in GCS, the output cannot be the gcs path, it has to be the local path (as mentioned in the notebook : `/app/df_train.csv`)

- It's very hard to cancel a running pipeline

- When a pipeline uses the same images as the previous run, the results will be retrieved from cache 

- You can clone a git repo directly from the notebook instance by clicking at the Git+ logo (at left)

- The `compiler` section will create a compressed `tar.gz` file that contains the pipeline. This can be shared to be deployed easily by other colleagues, stored in AI Hub, etc..

- For every step of the pipeline, there is Logs section that can help for debugging errors.

- Be careful to specify the region when you want to see deployed models in the user interface

- One the model is deployed, check this page for more info about predictions :
`https://cloud.google.com/ai-platform/prediction/docs/online-predict`

- Check this link for more tutorials : `https://github.com/kubeflow/pipelines/tree/master/samples/core/ai_platform` 