from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ne_investment.db"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "green_projects_sector_summary.csv"
)


def calculate_green_projects_sector_summary() -> pd.DataFrame:
    query = """
        SELECT
            sector,
            technology_theme,
            COUNT(*) AS projects,

            SUM(
                CASE
                    WHEN capital_value_status = 'committed'
                    THEN regional_capital_investment_gbp
                END
            ) AS committed_regional_capital_gbp,

            SUM(
                CASE
                    WHEN capital_value_status = 'potential'
                    THEN regional_capital_investment_gbp
                END
            ) AS potential_regional_capital_gbp,

            SUM(regional_economic_impact_gbp)
                AS regional_economic_impact_gbp,

            SUM(construction_jobs)
                AS construction_jobs,

            SUM(operational_jobs)
                AS operational_jobs,

            SUM(jobs_supported)
                AS jobs_supported,

            SUM(regional_jobs_announced)
                AS regional_jobs_announced,

            SUM(
                CASE delivery_risk_rating
                    WHEN 'low' THEN 1
                    ELSE 0
                END
            ) AS low_risk_projects,

            SUM(
                CASE delivery_risk_rating
                    WHEN 'medium' THEN 1
                    ELSE 0
                END
            ) AS medium_risk_projects,

            SUM(
                CASE delivery_risk_rating
                    WHEN 'high' THEN 1
                    ELSE 0
                END
            ) AS high_risk_projects

        FROM green_investment_projects_view

        GROUP BY
            sector,
            technology_theme

        ORDER BY
            committed_regional_capital_gbp DESC,
            projects DESC,
            sector,
            technology_theme
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(
            query,
            connection,
        )

    return dataframe


if __name__ == "__main__":
    result = calculate_green_projects_sector_summary()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(result.to_string(index=False))
    print(f"\nSaved sector summary to: {OUTPUT_PATH}")

