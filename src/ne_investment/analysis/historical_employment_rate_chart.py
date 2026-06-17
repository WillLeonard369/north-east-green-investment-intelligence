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
    / "historical_employment_rate_comparison.png"
)


def create_historical_employment_rate_chart() -> None:
    query = """
        SELECT
            geography_name,
            period,
            value
        FROM historical_regional_labour_market
        WHERE indicator_code = 'EMPLOYMENT_RATE'
        ORDER BY geography_name, period
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(query, connection)

    dataframe["period_start"] = pd.to_datetime(
        dataframe["period"].str.extract(
            r"^([A-Z][a-z]{2} \d{4})"
        )[0],
        format="%b %Y",
    )

    plt.figure(figsize=(11, 6))

    for geography_name, group in dataframe.groupby("geography_name"):
        group = group.sort_values("period_start")

        plt.plot(
            group["period_start"],
            group["value"],
            label=geography_name,
        )

    plt.title("Employment Rate: North East vs North West")
    plt.xlabel("Period")
    plt.ylabel("Employment rate (%)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300)
    plt.close()

    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_historical_employment_rate_chart()