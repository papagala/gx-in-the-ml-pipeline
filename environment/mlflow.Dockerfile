# Use Python 3.11.10 as the base image
FROM python:3.11.10-bookworm

# Set environment variables for non-interactive installations
ENV DEBIAN_FRONTEND=noninteractive
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

# Install necessary system dependencies and pyenv dependencies
RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    curl \
    git \
    vim \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pyenv
RUN git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT && \
    echo 'eval "$(pyenv init -)"' >> /root/.bashrc

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose MLflow server port
EXPOSE 5000

# Command to start the MLflow server
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]
