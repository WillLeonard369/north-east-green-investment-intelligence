from pathlib import Path

import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "green_projects"
    / "project_template.csv"
)

SECTORS_FILE = PROJECT_ROOT / "config" / "sectors.yml"

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


def load_sector_taxonomy() -> dict:
    with SECTORS_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def canonicalise_values(
    dataframe: pd.DataFrame,
    column: str,
    valid_values: list[str],
) -> None:
    canonical_lookup = {
        value.strip().lower(): value
        for value in valid_values
    }

    supplied_values = (
        dataframe[column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    invalid_values = {
        value
        for value in supplied_values
        if value.lower() not in canonical_lookup
    }

    if invalid_values:
        raise ValueError(
            f"Invalid values in {column}: {sorted(invalid_values)}"
        )

    dataframe[column] = dataframe[column].apply(
        lambda value: (
            canonical_lookup[str(value).strip().lower()]
            if pd.notna(value)
            else value
        )
    )


def transform_green_projects() -> pd.DataFrame:
    dataframe = pd.read_csv(SOURCE_FILE)

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required project columns: {sorted(missing_columns)}"
        )

    taxonomy = load_sector_taxonomy()

    valid_sectors = [
        details["label"]
        for details in taxonomy["sectors"].values()
    ]

    valid_technology_themes = [
        theme
        for details in taxonomy["sectors"].values()
        for theme in details["technology_themes"]
    ]

    canonicalise_values(
        dataframe,
        "sector",
        valid_sectors,
    )

    canonicalise_values(
        dataframe,
        "technology_theme",
        valid_technology_themes,
    )

    canonicalise_values(
        dataframe,
        "regional_linkage_type",
        taxonomy["regional_linkage_types"],
    )

    canonicalise_values(
        dataframe,
        "regional_linkage_strength",
        taxonomy["regional_linkage_strengths"],
    )

    canonicalise_values(
        dataframe,
        "project_status",
        taxonomy["project_statuses"],
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
        "technology_theme",
        "project_status",
        "regional_linkage_type",
        "regional_linkage_strength",
        "source_name",
    ]

    for column in required_non_null:
        if dataframe[column].isna().any():
            raise ValueError(f"Missing required values in {column}.")

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