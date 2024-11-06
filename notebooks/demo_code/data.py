import io
import pathlib
import random
import shutil
import zipfile

import pandas as pd
import requests
import ucimlrepo

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


def get_new_patient_data() -> pd.DataFrame:
    random.seed(42)

    df = ucimlrepo.fetch_ucirepo(id=45).data.features
    df["age"] = df["age"].apply(lambda x: x + random.randrange(1, 10, 1))
    df["age"] = df["age"].apply(lambda x: random.randrange(25, 79, 1) if x >= 80 else x)

    return df
