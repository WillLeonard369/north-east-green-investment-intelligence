from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def calculate_ashe_earnings_gap() -> pd.DataFrame:
    query = """
        SELECT
            geography_name,
            indicator_code,
            period,
            value
        FROM regional_earnings_view
        ORDER BY indicator_code, period, geography_name
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(query, connection)

    pivot = dataframe.pivot_table(
        index=["indicator_code", "period"],
        columns="geography_name",
        values="value",
        aggfunc="first",
    ).reset_index()

    pivot["absolute_gap"] = (
        pivot["North West"] - pivot["North East"]
    )

    pivot["north_east_gap_pct"] = (
        (pivot["North East"] / pivot["North West"]) - 1
    ) * 100

    return pivot.sort_values(
        ["indicator_code", "period"]
    ).reset_index(drop=True)


if __name__ == "__main__":
    result = calculate_ashe_earnings_gap()
    print(result.tail(20).to_string(index=False))