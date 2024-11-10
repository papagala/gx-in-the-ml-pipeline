# gx-in-the-ml-pipeline

This repo hosts demo code used illustrate how GX can be integrated into the MLOps lifecycle.

## Known limitations
* The demo notebooks and environment are current as of 2024-11-12 and are not currently actively maintained.

* This demo is compatible with an [agent-enabled deployment](https://docs.greatexpectations.io/docs/cloud/deploy/deployment_patterns#agent-enabled-deployment) of GX Cloud. The Docker compose environment requires a GX Cloud [organization id and access token](https://docs.greatexpectations.io/docs/cloud/connect/connect_python#get-your-user-access-token-and-organization-id) to run. These credentials must be provided as `GX_CLOUD_ORGANIZATION_ID` and `GX_CLOUD_ACCESS_TOKEN` environment variables to Docker compose.


## Quickstart

1. Clone this repo locally.
   ```
   git clone https://github.com/rachhouse/gx-in-the-ml-pipeline.git
   ```

2. Change directory into the repo root directory.
   ```
   cd gx-in-the-ml-pipeline
   ```

3. Start the containerized environment using Docker compose. `YOUR_GX_CLOUD_ORG_ID_ENVVAR_NAME` and `YOUR_GX_CLOUD_ACCESS_TOKEN_ENVVAR_NAME` should be replaced by the names of the environment variables containing your GX Cloud org id and access token, respectively:
   ```
   GX_CLOUD_ORGANIZATION_ID=${YOUR_GX_CLOUD_ORG_ID_ENVVAR_NAME} GX_CLOUD_ACCESS_TOKEN=${YOUR_GX_CLOUD_ACCESS_TOKEN_ENVVAR_NAME} docker compose up --build
   ```

4. Access the running servers:
  * JupyterLab: [http://localhost:8888/lab](http://localhost:8888/lab)
  * MLflow Tracking Server: [http://localhost:5000](http://localhost:5000)


5. Once you are finished running the containerized environment, stop it using Docker compose.
   ```
   GX_CLOUD_ORGANIZATION_ID=${YOUR_GX_CLOUD_ORG_ID_ENVVAR_NAME} GX_CLOUD_ACCESS_TOKEN=${YOUR_GX_CLOUD_ACCESS_TOKEN_ENVVAR_NAME} docker compose down --volumes
   ```