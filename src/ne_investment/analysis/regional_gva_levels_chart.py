from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"
OUTPUT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "figures"
    / "regional_real_gva_levels.png"
)


def create_regional_gva_levels_chart() -> None:
    query = """
        SELECT
            geography_name,
            period,
            value
        FROM regional_gva_levels
        ORDER BY geography_name, period
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(query, connection)

    dataframe["period"] = dataframe["period"].astype(int)
    dataframe["value_billions"] = dataframe["value"] / 1000

    plt.figure(figsize=(10, 6))

    for geography_name, group in dataframe.groupby("geography_name"):
        plt.plot(
            group["period"],
            group["value_billions"],
            label=geography_name,
        )

    plt.title("Real GVA Levels: North East vs North West")
    plt.xlabel("Year")
    plt.ylabel("£ billion, 2022 prices")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300)
    plt.close()

    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_regional_gva_levels_chart()