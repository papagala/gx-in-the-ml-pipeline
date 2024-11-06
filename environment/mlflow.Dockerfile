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

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install virtualenv

# Run MLflow tracking server.
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]