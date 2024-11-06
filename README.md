# gx-in-the-ml-pipeline

This repo hosts demo code used illustrate how GX can be integrated into the MLOps lifecycle. It is current as of 2024-11-12 and is not actively maintained.

## Quickstart

1. Clone this repo locally.
   ```
   git clone https://github.com/rachhouse/gx-in-the-ml-pipeline.git
   ```

2. Change directory into the repo root directory.
   ```
   cd gx-in-the-ml-pipeline
   ```

3. Start the containerized environment using Docker compose.
   ```
   docker compose up --build
   ```

4. Access the running servers:
  * JupyterLab: [http://localhost:8888/lab](http://localhost:8888/lab)
  * MLflow Tracking Server: [http://localhost:5000](http://localhost:5000)


5. Once you are finished running the containerized environment, stop it using Docker compose.
   ```
   docker compose down --volumes
   ```