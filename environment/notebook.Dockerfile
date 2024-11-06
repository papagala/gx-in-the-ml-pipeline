FROM ubuntu:22.04

USER root
ENV DEBIAN_FRONTEND noninteractive
ENV ROOT_HOME /root

RUN apt-get update && \
    apt-get -y install \
        apt-utils \
        build-essential \
        curl \
        git \
        iputils-ping \
        jq \
        libbz2-dev \
        libffi-dev \
        liblzma-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        sudo \
        wget \
        vim \
        zip \
        zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

RUN curl https://pyenv.run | bash

ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

ENV PYTHON_VERSION 3.11.10
RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION

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