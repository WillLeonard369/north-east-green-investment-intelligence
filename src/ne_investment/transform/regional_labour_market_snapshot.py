from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "ons"
    / "labour_market"
    / "lmregsummarymay2026.xls"
)

REGIONS = {
    "E12000001": "North East",
    "E12000002": "North West",
}


def transform_regional_labour_market_snapshot() -> pd.DataFrame:
    dataframe = pd.read_excel(
        SOURCE_FILE,
        sheet_name="S01.1",
        header=7,
    )

    regional_rows = (
        dataframe[dataframe["Area Codes"].isin(REGIONS)]
        .drop_duplicates(subset=["Area Codes"], keep="first")
        .copy()
    )

    indicator_columns = {
        "ECONOMIC_ACTIVITY_RATE": "Rate (%)2",
        "EMPLOYMENT_RATE": "Rate (%)2.1",
        "UNEMPLOYMENT_RATE": "Rate (%)3",
        "ECONOMIC_INACTIVITY_RATE": "Rate (%)2.2",
    }

    output_rows = []

    for _, row in regional_rows.iterrows():
        geography_code = row["Area Codes"]

        for indicator_code, source_column in indicator_columns.items():
            output_rows.append(
                {
                    "geography_code": geography_code,
                    "geography_name": REGIONS[geography_code],
                    "indicator_code": indicator_code,
                    "period": "2026-Q1",
                    "frequency": "quarterly_snapshot",
                    "value": row[source_column],
                    "unit": "percent",
                }
            )

    output = pd.DataFrame(output_rows)
    output["value"] = pd.to_numeric(output["value"], errors="coerce")

    if output["value"].isna().any():
        raise ValueError("Missing or invalid labour-market values found.")

    if output.duplicated(
        ["geography_code", "indicator_code", "period"]
    ).any():
        raise ValueError("Duplicate labour-market observations found.")

    return output


if __name__ == "__main__":
    result = transform_regional_labour_market_snapshot()
    print(result.to_string(index=False))