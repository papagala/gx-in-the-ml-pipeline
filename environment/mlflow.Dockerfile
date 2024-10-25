FROM python:3.11-slim

RUN pip install mlflow

# Run MLflow tracking server.
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]
