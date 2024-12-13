# Use Python 3.11.10 as the base image
FROM python:3.11.10-bookworm

# Set environment variables for non-interactive installations
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary system dependencies
RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    build-essential \
    curl \
    git \
    vim \
    zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set up the working directory and copy dependencies
WORKDIR /app
COPY pyproject.toml ./

# Install dependencies with Poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Install JupyterLab and link the Poetry environment to an IPython kernel
RUN pip install jupyterlab ipykernel && \
    python -m ipykernel install --user --name=gx-in-the-ml-pipeline

# Copy local notebooks into image
COPY notebooks/ /notebooks/

# Use the /notebooks directory for JupyterLab
WORKDIR /notebooks

# Expose port 8888 for JupyterLab
EXPOSE 8888

# Command to start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--ServerApp.token=''", "--ServerApp.password=''"]