from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "green_projects"
    / "project_template.csv"
)

REQUIRED_COLUMNS = {
    "project_name",
    "project_type",
    "sector",
    "technology_theme",
    "geography_code",
    "location_name",
    "developer_name",
    "investor_name",
    "announcement_date",
    "expected_completion_date",
    "project_status",
    "regional_linkage_type",
    "regional_linkage_strength",
    "total_project_value_gbp",
    "regional_value_gbp",
    "total_jobs_announced",
    "regional_jobs_announced",
    "capacity_value",
    "capacity_unit",
    "source_name",
    "source_url",
    "retrieved_at",
    "notes",
}


def transform_green_projects() -> pd.DataFrame:
    dataframe = pd.read_csv(SOURCE_FILE)

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required project columns: {sorted(missing_columns)}"
        )

    numeric_columns = [
        "total_project_value_gbp",
        "regional_value_gbp",
        "total_jobs_announced",
        "regional_jobs_announced",
        "capacity_value",
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

    date_columns = [
        "announcement_date",
        "expected_completion_date",
        "retrieved_at",
    ]

    for column in date_columns:
        dataframe[column] = pd.to_datetime(
            dataframe[column],
            errors="coerce",
        ).dt.strftime("%Y-%m-%d")

    required_non_null = [
        "project_name",
        "project_type",
        "sector",
        "project_status",
        "regional_linkage_type",
        "regional_linkage_strength",
        "source_name",
    ]

    for column in required_non_null:
        if dataframe[column].isna().any():
            raise ValueError(f"Missing required values in {column}.")

    valid_strengths = {"direct", "significant", "indirect"}

    invalid_strengths = set(
        dataframe["regional_linkage_strength"].dropna().str.lower()
    ).difference(valid_strengths)

    if invalid_strengths:
        raise ValueError(
            f"Invalid regional linkage strengths: {sorted(invalid_strengths)}"
        )

    if dataframe.duplicated(
        [
            "project_name",
            "developer_name",
            "announcement_date",
        ]
    ).any():
        raise ValueError("Duplicate green-investment projects found.")

    return dataframe


if __name__ == "__main__":
    result = transform_green_projects()
    print(result.to_string(index=False))