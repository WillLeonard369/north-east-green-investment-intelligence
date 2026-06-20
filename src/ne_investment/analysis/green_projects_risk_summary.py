from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def calculate_green_projects_risk_summary() -> pd.DataFrame:
    query = """
        SELECT
            delivery_risk_rating,
            COUNT(*) AS projects,
            SUM(
                CASE
                    WHEN capital_value_status = 'committed'
                    THEN regional_capital_investment_gbp
                END
            ) AS committed_capital_gbp,
            SUM(
                CASE
                    WHEN capital_value_status = 'estimated'
                    THEN regional_capital_investment_gbp
                END
            ) AS estimated_capital_gbp,
            SUM(
                CASE
                    WHEN capital_value_status = 'potential'
                    THEN regional_capital_investment_gbp
                END
            ) AS potential_capital_gbp
        FROM green_investment_projects_view
        GROUP BY delivery_risk_rating
        ORDER BY
            CASE delivery_risk_rating
                WHEN 'low' THEN 1
                WHEN 'medium' THEN 2
                WHEN 'high' THEN 3
            END
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(query, connection)

    return dataframe


if __name__ == "__main__":
    result = calculate_green_projects_risk_summary()
    print(result.to_string(index=False))