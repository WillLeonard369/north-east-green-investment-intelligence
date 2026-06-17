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
    / "verified_green_projects_portfolio.png"
)


def create_green_projects_chart() -> None:
    query = """
        SELECT
            project_name,
            regional_value_gbp,
            regional_jobs_announced
        FROM green_investment_projects_view
        WHERE regional_value_gbp IS NOT NULL
        ORDER BY regional_value_gbp ASC
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        dataframe = pd.read_sql_query(query, connection)

    dataframe["regional_value_gbp_millions"] = (
        dataframe["regional_value_gbp"] / 1_000_000
    )

    plt.figure(figsize=(11, 6))
    plt.barh(
        dataframe["project_name"],
        dataframe["regional_value_gbp_millions"],
    )
    plt.title("Verified North East Green Investment Projects")
    plt.xlabel("Verified regional investment (£ million)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300)
    plt.close()

    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_green_projects_chart()