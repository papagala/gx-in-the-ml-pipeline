import collections
import io
import pathlib
import random
import shutil
import zipfile
from typing import Dict, List, Tuple, Union

import great_expectations as gx
import pandas as pd
import requests
import sqlalchemy
import ucimlrepo

import demo_code.log as logger

log = logger.get_logger()

POSTGRES_CONNECTION_STRING = "postgresql://gx_user:gx_user_password@postgres:5432/demo"

COL2DESCRIPTION = collections.OrderedDict(
    {
        "age": "Age in years",
        "sex": "sex; 1: male, 0: female",
        "cp": "Chest pain type; 1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic",
        "trestbps": "Resting blood pressure in mm Hg on admission to the hospital",
        "chol": "Serum cholesterol in mg/dl",
        "fbs": "Fasting blood sugar > 120 mg/dl; 1: true, 0: false",
        "restecg": "Resting electrocardiographic results; 0: normal, 1: having ST-T wave abnormality, 2: showing probable or definite left ventricular hypertrophy",
        "thalach": "Maximum heart rate achieved",
        "exang": "Exercise induced angina; 1: yes, 0: no",
        "oldpeak": "ST depression induced by exercise relative to rest",
        "slope": "Slope of the peak exercise ST segment; 1: upsloping, 2: flat, 3: downsloping",
        "ca": "Major vessels (0-3) colored by flourosopy",
        "thal": "Heart defect; 3 = normal; 6 = fixed defect; 7 = reversable defect",
        "num": "Diagnosis of heart disease (target label); 0: no heart disease present, 1: heart disease present",
    }
)


COLUMNS = list(COL2DESCRIPTION.keys())

DATASET_NAME2FILE = {
    "va": "processed.va.data",
    "hungarian": "processed.hungarian.data",
    "switzerland": "processed.switzerland.data",
    "cleveland": "processed.cleveland.data",
}

MOSTLY = 0.9

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
]


def download_uci_heart_disease_data(data_dir: pathlib.Path, force: bool) -> None:
    """Download sample heart disease data from UCI ML Repository."""

    if force:
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


def load_uci_heart_disease_data(data_dir: pathlib.Path) -> pd.DataFrame:
    """Return sample heart disease data from UCI ML Repository as pandas DataFame."""
    samples = []

    # Sample data is split across datasets gathered from four health centers.
    for dataset_name, dataset_file in DATASET_NAME2FILE.items():
        df_dataset = pd.read_csv(data_dir / dataset_file, names=COLUMNS)
        df_dataset["dataset"] = dataset_name
        samples.append(df_dataset)

    df = pd.concat(samples)
    df = df.drop(columns=["dataset"])

    return df


def display_heart_disease_data_dictionary() -> pd.DataFrame:
    """Return data dictionary for heart disease data as pandas DataFrame."""

    data_dict = []
    for k, v in COL2DESCRIPTION.items():
        data_dict.append({"variable name": k, "variable description": v})

    return pd.DataFrame(data_dict)


def get_new_patient_data() -> pd.DataFrame:
    """Return "new" patient data (for data drift detection) as pandas DataFrame."""
    random.seed(42)

    df = ucimlrepo.fetch_ucirepo(id=45).data.features
    df["age"] = df["age"].apply(lambda x: x + random.randrange(1, 10, 1))
    df["age"] = df["age"].apply(lambda x: random.randrange(25, 79, 1) if x >= 80 else x)

    return df


def clean_question_mark_for_float_columns(x: str) -> Union[float, None]:
    """Nullify question marks and return figures as floats."""
    x = str(x).strip()
    if x == "?":
        return None
    else:
        return float(x)


def clean_question_mark_for_int_columns(x: str) -> Union[int, None]:
    """Nullify question marks and return figures as int."""
    x = str(x).strip()
    if x == "?":
        return None
    else:
        return int(float(x))


def generate_distribution_bins_and_weights_for_age_column(
    df: pd.DataFrame,
) -> Tuple[Dict, Dict]:
    """Generate bins and weights for the age column."""
    bins, weights = [], []
    min_age, max_age = 25, 80

    for x in range(min_age, max_age, 5):
        bin_count = df[(df["age"] >= x) & (df["age"] < x + 5)].shape[0]
        proportion = round(bin_count / df.shape[0], 3)
        log.debug(f"{x}-{x+5}:\t{bin_count}\t{proportion}")
        bins.append(x)
        weights.append(proportion)

    bins.append(max_age)

    return bins, weights


def write_df_to_postgres(table_name: str, df: pd.DataFrame) -> int:
    """Write dataframe data to a postgres table."""

    engine = sqlalchemy.create_engine(POSTGRES_CONNECTION_STRING)
    rows_written = df.to_sql(table_name, engine, if_exists="replace", index=False)

    return rows_written


def clean_demo_data_from_gx_cloud_org(
    context: gx.data_context.CloudDataContext,
    data_source_name: str,
    expectation_suite_names: List[str],
    validation_definition_names: List[str],
    checkpoint_names: List[str],
):
    """Delete specified demo data from the GX Cloud organization provided by the context."""
    # Remove Checkpoint.
    cloud_checkpoints = [x.name for x in context.checkpoints.all()]
    log.debug(f"Found GX Cloud Checkpoints: {cloud_checkpoints}")

    for x in checkpoint_names:
        if x in cloud_checkpoints:
            context.checkpoints.delete(name=x)
            log.info(f"Removed Checkpoint: {x}")

    # Remove Validation Definitions.
    cloud_validation_definitions = [
        x.name for x in context.validation_definitions.all()
    ]
    log.debug(f"Found GX Cloud validation definitions: {cloud_validation_definitions}")

    for x in validation_definition_names:
        if x in cloud_validation_definitions:
            try:
                context.validation_definitions.delete(name=x)
                log.info(f"Removed Validation Definition: {x}")
            except:
                log.warning(f"Could not remove {x}")

    # Remove Expectation Suites.
    cloud_suites = [x["name"] for x in context.suites.all()]
    log.debug(f"Found GX Cloud Expectation Suites: {cloud_suites}")

    for x in expectation_suite_names:
        if x in cloud_suites:
            context.suites.delete(name=x)
            log.info(f"Removed Expectation Suite: {x}")

    # Remove Data Source.
    cloud_data_sources = list(context.data_sources.all().keys())
    log.debug(f"Found GX Cloud Data Sources: {cloud_data_sources}")
    data_source_name = "demo database"

    if data_source_name in cloud_data_sources:
        context.data_sources.delete(name=data_source_name)
        log.info(f"Removed Data Source: {data_source_name}")
