from pathlib import Path

import matplotlib.pyplot as plt

from src.ne_investment.analysis.green_projects_sector_summary import (
    calculate_green_projects_sector_summary,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "figures"
    / "green_projects_capital_by_theme.png"
)


def create_green_projects_sector_chart() -> None:
    dataframe = calculate_green_projects_sector_summary()

    chart_data = dataframe.copy()

    chart_data["committed_capital_millions"] = (
        chart_data["committed_regional_capital_gbp"].fillna(0)
        / 1_000_000
    )

    chart_data["potential_capital_millions"] = (
        chart_data["potential_regional_capital_gbp"].fillna(0)
        / 1_000_000
    )

    chart_data["label"] = (
        chart_data["sector"]
        + " — "
        + chart_data["technology_theme"]
    )

    chart_data = chart_data.sort_values(
        [
            "committed_capital_millions",
            "potential_capital_millions",
        ],
        ascending=True,
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(figsize=(12, 8))

    plt.barh(
        chart_data["label"],
        chart_data["committed_capital_millions"],
        label="Committed regional capital",
    )

    plt.barh(
        chart_data["label"],
        chart_data["potential_capital_millions"],
        left=chart_data["committed_capital_millions"],
        label="Potential regional capital",
    )

    plt.title(
        "North East Green Investment Capital by Technology Theme"
    )
    plt.xlabel("Regional capital investment (£ million)")
    plt.ylabel("")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        OUTPUT_PATH,
        dpi=300,
    )
    plt.close()

    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_green_projects_sector_chart()