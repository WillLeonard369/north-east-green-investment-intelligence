from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def calculate_green_projects_summary() -> pd.DataFrame:
    query = """
        SELECT
            project_name,
            capital_value_status,
            regional_capital_investment_gbp,
            regional_economic_impact_gbp,
            construction_jobs,
            operational_jobs,
            jobs_supported,
            regional_jobs_announced
        FROM green_investment_projects_view
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

    committed_capital = dataframe.loc[
        dataframe["capital_value_status"] == "committed",
        "regional_capital_investment_gbp",
    ].sum(min_count=1)

    estimated_capital = dataframe.loc[
        dataframe["capital_value_status"] == "estimated",
        "regional_capital_investment_gbp",
    ].sum(min_count=1)

    potential_capital = dataframe.loc[
        dataframe["capital_value_status"] == "potential",
        "regional_capital_investment_gbp",
    ].sum(min_count=1)

    summary = pd.DataFrame(
        {
            "metric": [
                "projects",
                "committed_regional_capital_investment_gbp",
                "estimated_regional_capital_investment_gbp",
                "potential_regional_capital_investment_gbp",
                "regional_economic_impact_gbp",
                "construction_jobs",
                "operational_jobs",
                "jobs_supported",
                "regional_jobs_announced",
            ],
            "value": [
                len(dataframe),
                committed_capital,
                estimated_capital,
                potential_capital,
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