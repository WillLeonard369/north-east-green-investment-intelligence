from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def calculate_bres_employment_growth() -> pd.DataFrame:
    query = """
        SELECT
            geography_name,
            industry_code,
            industry_name,
            period,
            value
        FROM bres_industry_employment
        WHERE period IN ('2015', '2024')
        ORDER BY
            geography_name,
            industry_code,
            period
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(query, connection)

    pivot = dataframe.pivot_table(
        index=[
            "geography_name",
            "industry_code",
            "industry_name",
        ],
        columns="period",
        values="value",
        aggfunc="first",
    ).reset_index()

    pivot["absolute_change"] = pivot["2024"] - pivot["2015"]
    pivot["growth_pct"] = (
        (pivot["2024"] / pivot["2015"]) - 1
    ) * 100

    return pivot.sort_values(
        ["geography_name", "growth_pct"],
        ascending=[True, False],
    )


if __name__ == "__main__":
    result = calculate_bres_employment_growth()
    print(result.to_string(index=False))