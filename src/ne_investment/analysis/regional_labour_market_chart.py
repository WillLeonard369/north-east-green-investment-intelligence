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
    / "regional_labour_market_snapshot.png"
)


def create_regional_labour_market_chart() -> None:
    query = """
        SELECT
            geography_name,
            indicator_code,
            value
        FROM regional_labour_market_snapshot
        ORDER BY geography_name, indicator_code
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(query, connection)

    indicator_labels = {
        "ECONOMIC_ACTIVITY_RATE": "Economic activity",
        "EMPLOYMENT_RATE": "Employment",
        "UNEMPLOYMENT_RATE": "Unemployment",
        "ECONOMIC_INACTIVITY_RATE": "Economic inactivity",
    }

    dataframe["indicator_label"] = dataframe["indicator_code"].map(
        indicator_labels
    )

    chart_data = dataframe.pivot(
        index="indicator_label",
        columns="geography_name",
        values="value",
    )

    chart_data = chart_data.reindex(
        [
            "Economic activity",
            "Employment",
            "Unemployment",
            "Economic inactivity",
        ]
    )

    chart_data.plot(
        kind="bar",
        figsize=(10, 6),
    )

    plt.title("Regional Labour Market Snapshot, 2026 Q1")
    plt.xlabel("")
    plt.ylabel("Percent")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300)
    plt.close()

    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_regional_labour_market_chart()