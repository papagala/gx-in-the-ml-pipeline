import io
import pathlib
import shutil
import zipfile

import requests

import demo_code.log as logger

log = logger.get_logger()

CLEANED_COLUMNS = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
    "dataset",
    "num",
]

FEATURE_COLUMNS = [
    "age",
    "sex",
    "cp_0",
    "cp_1",
    "cp_2",
    "cp_3",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
    "num",
]


def download_uci_heart_disease_data(data_dir: pathlib.Path) -> None:
    """Download sample heart disease data from UCI ML Repository."""

    data_url = "https://archive.ics.uci.edu/static/public/45/heart+disease.zip"

    response = requests.get(data_url)

    log.debug("Fetching data...")
    if response.status_code == 200:
        shutil.rmtree(data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(response.content)) as fh:
            fh.extractall(data_dir)
            log.debug("Downloaded data.")
    else:
        log.error(f"Failed to download data: {response.status_code}")
