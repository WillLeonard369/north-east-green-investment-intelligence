from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def analyse_gva() -> pd.DataFrame:
    query = """
        SELECT
            period,
            value
        FROM north_east_gva
        ORDER BY period
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(query, connection)

    dataframe["period"] = dataframe["period"].astype(int)
    dataframe["annual_growth_pct"] = dataframe["value"].pct_change() * 100

    return dataframe


if __name__ == "__main__":
    result = analyse_gva()
    print(result.tail(10).to_string(index=False))