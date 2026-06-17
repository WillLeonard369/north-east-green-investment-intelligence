from pathlib import Path

import matplotlib.pyplot as plt

from src.ne_investment.analysis.bres_employment_growth import (
    calculate_bres_employment_growth,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "figures"
    / "north_east_bres_employment_growth.png"
)


def create_bres_employment_growth_chart() -> None:
    dataframe = calculate_bres_employment_growth()

    north_east = dataframe[
        dataframe["geography_name"] == "North East"
    ].copy()

    north_east = north_east.sort_values(
        "growth_pct",
        ascending=True,
    )

    plt.figure(figsize=(11, 8))
    plt.barh(
        north_east["industry_name"],
        north_east["growth_pct"],
    )
    plt.axvline(0, linewidth=1)
    plt.title("North East Employment Growth by Industry, 2015–2024")
    plt.xlabel("Employment growth (%)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300)
    plt.close()

    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_bres_employment_growth_chart()