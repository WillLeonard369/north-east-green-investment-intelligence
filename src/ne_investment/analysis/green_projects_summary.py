from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def calculate_green_projects_summary() -> pd.DataFrame:
    query = """
        SELECT
            project_name,
            project_type,
            sector,
            technology_theme,
            location_name,
            regional_linkage_type,
            regional_linkage_strength,
            regional_capital_investment_gbp,
            regional_economic_impact_gbp,
            construction_jobs,
            operational_jobs,
            jobs_supported,
            regional_jobs_announced,
            project_status
        FROM green_investment_projects_view
        ORDER BY regional_capital_investment_gbp DESC
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(query, connection)

    numeric_columns = [
        "regional_capital_investment_gbp",
        "regional_economic_impact_gbp",
        "construction_jobs",
        "operational_jobs",
        "jobs_supported",
        "regional_jobs_announced",
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

    summary = pd.DataFrame(
        {
            "metric": [
                "projects",
                "verified_regional_capital_investment_gbp",
                "regional_economic_impact_gbp",
                "construction_jobs",
                "operational_jobs",
                "jobs_supported",
                "regional_jobs_announced",
            ],
            "value": [
                len(dataframe),
                dataframe[
                    "regional_capital_investment_gbp"
                ].sum(min_count=1),
                dataframe[
                    "regional_economic_impact_gbp"
                ].sum(min_count=1),
                dataframe["construction_jobs"].sum(min_count=1),
                dataframe["operational_jobs"].sum(min_count=1),
                dataframe["jobs_supported"].sum(min_count=1),
                dataframe[
                    "regional_jobs_announced"
                ].sum(min_count=1),
            ],
        }
    )

    return summary


if __name__ == "__main__":
    result = calculate_green_projects_summary()
    print(result.to_string(index=False))