FROM python:3.11-slim

# Requirements to run JupyterLab and install kernel for the poetry env.
RUN pip install poetry ipykernel ipython jupyter jupyterlab

# Install dependencies using poetry and create an ipykernel for poetry env.
COPY pyproject.toml pyproject.toml
RUN poetry install
RUN poetry run python -m ipykernel install --user --name=gx-in-the-ml-pipeline

# Use notebooks subdirectory for JupyterLab.
WORKDIR /notebooks

# Start JupyterLab, access via localhost:8888 in a host web browser.
ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]