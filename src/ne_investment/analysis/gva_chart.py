from pathlib import Path

import matplotlib.pyplot as plt

from src.ne_investment.analysis.gva_analysis import analyse_gva


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = PROJECT_ROOT / "reports" / "figures" / "north_east_gva_index.png"


def create_gva_chart() -> None:
    dataframe = analyse_gva()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(dataframe["period"], dataframe["value"])
    plt.title("North East Real GVA Index")
    plt.xlabel("Year")
    plt.ylabel("Index, 2022 = 100")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300)
    plt.close()

    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_gva_chart()