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
    "announced_value_gbp",
    "jobs_announced",
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

    dataframe["announced_value_gbp"] = pd.to_numeric(
        dataframe["announced_value_gbp"],
        errors="coerce",
    )

    dataframe["jobs_announced"] = pd.to_numeric(
        dataframe["jobs_announced"],
        errors="coerce",
    )

    dataframe["capacity_value"] = pd.to_numeric(
        dataframe["capacity_value"],
        errors="coerce",
    )

    dataframe["announcement_date"] = pd.to_datetime(
        dataframe["announcement_date"],
        errors="coerce",
    ).dt.strftime("%Y-%m-%d")

    dataframe["expected_completion_date"] = pd.to_datetime(
        dataframe["expected_completion_date"],
        errors="coerce",
    ).dt.strftime("%Y-%m-%d")

    dataframe["retrieved_at"] = pd.to_datetime(
        dataframe["retrieved_at"],
        errors="coerce",
    ).dt.strftime("%Y-%m-%d")

    if dataframe["project_name"].isna().any():
        raise ValueError("Missing project names found.")

    if dataframe["source_name"].isna().any():
        raise ValueError("Missing project source names found.")

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