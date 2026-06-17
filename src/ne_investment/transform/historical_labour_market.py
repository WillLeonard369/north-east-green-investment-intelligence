from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "nomis"
    / "labour_market"
    / "labourforce.xlsx"
)

REGION_BLOCKS = {
    "E12000001": {
        "name": "North East",
        "start_row": 9,
        "end_row": 425,
    },
    "E12000002": {
        "name": "North West",
        "start_row": 430,
        "end_row": None,
    },
}


def transform_historical_labour_market() -> pd.DataFrame:
    raw = pd.read_excel(
        SOURCE_FILE,
        sheet_name="Data",
        header=None,
    )

    output_rows = []

    for geography_code, metadata in REGION_BLOCKS.items():
        block = raw.iloc[
            metadata["start_row"]:metadata["end_row"],
            [0, 5, 6, 7, 8],
        ].copy()

        block.columns = [
            "period",
            "economic_activity_rate",
            "employment_rate",
            "unemployment_rate",
            "economic_inactivity_rate",
        ]

        block = block[
            block["period"]
            .astype(str)
            .str.match(
                r"^[A-Z][a-z]{2} \d{4}-[A-Z][a-z]{2} \d{4}$",
                na=False,
            )
        ].copy()

        for _, row in block.iterrows():
            values = {
                "ECONOMIC_ACTIVITY_RATE": row["economic_activity_rate"],
                "EMPLOYMENT_RATE": row["employment_rate"],
                "UNEMPLOYMENT_RATE": row["unemployment_rate"],
                "ECONOMIC_INACTIVITY_RATE": row["economic_inactivity_rate"],
            }

            for indicator_code, value in values.items():
                output_rows.append(
                    {
                        "geography_code": geography_code,
                        "geography_name": metadata["name"],
                        "indicator_code": indicator_code,
                        "period": str(row["period"]),
                        "frequency": "rolling_3_month",
                        "value": value,
                        "unit": "percent",
                    }
                )

    output = pd.DataFrame(output_rows)
    output["value"] = pd.to_numeric(output["value"], errors="coerce")

    if output.empty:
        raise ValueError("No historical labour-market observations found.")

    if output["value"].isna().any():
        raise ValueError(
            "Missing or invalid historical labour-market values found."
        )

    if output.duplicated(
        ["geography_code", "indicator_code", "period"]
    ).any():
        raise ValueError(
            "Duplicate historical labour-market observations found."
        )

    return output


if __name__ == "__main__":
    result = transform_historical_labour_market()
    print(result.head(20).to_string(index=False))
    print(f"\nRows: {len(result)}")