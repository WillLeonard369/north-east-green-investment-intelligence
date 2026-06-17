from pathlib import Path

import matplotlib.pyplot as plt

from src.ne_investment.analysis.ashe_earnings_gap import (
    calculate_ashe_earnings_gap,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "figures"
    / "north_east_earnings_gap.png"
)


def create_ashe_earnings_gap_chart() -> None:
    dataframe = calculate_ashe_earnings_gap()

    weekly = dataframe[
        dataframe["indicator_code"] == "MEDIAN_WEEKLY_GROSS_PAY"
    ].copy()

    weekly["period"] = weekly["period"].astype(int)

    plt.figure(figsize=(10, 6))
    plt.plot(
        weekly["period"],
        weekly["north_east_gap_pct"],
    )
    plt.axhline(0, linewidth=1)
    plt.title("North East Median Weekly Pay Gap vs North West")
    plt.xlabel("Year")
    plt.ylabel("North East shortfall relative to North West (%)")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300)
    plt.close()

    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_ashe_earnings_gap_chart()