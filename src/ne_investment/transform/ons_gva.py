from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "ons"
    / "regionalgrossvalueaddedbalancedbyindustryandallinternationalterritoriallevelsitlregions.xlsx"
)

REGIONS = {
    "TLC": "North East",
    "TLD": "North West",
}


def transform_regional_gva() -> pd.DataFrame:
    dataframe = pd.read_excel(
        SOURCE_FILE,
        sheet_name="Table 1a",
        header=1,
    )

    regional_totals = dataframe[
        dataframe["ITL code"].isin(REGIONS)
        & (dataframe["SIC07 code"] == "Total")
    ].copy()

    year_columns = [
        column
        for column in dataframe.columns
        if str(column).isdigit()
    ]

    output_rows = []

    for _, row in regional_totals.iterrows():
        geography_code = row["ITL code"]

        for year in year_columns:
            output_rows.append(
                {
                    "geography_code": geography_code,
                    "geography_name": REGIONS[geography_code],
                    "indicator_code": "REAL_GVA_INDEX",
                    "period": str(year),
                    "frequency": "annual",
                    "value": row[year],
                    "unit": "index_2022_100",
                }
            )

    output = pd.DataFrame(output_rows)
    output["value"] = pd.to_numeric(output["value"], errors="coerce")

    if output["value"].isna().any():
        raise ValueError("Missing or invalid GVA values found.")

    if output.duplicated(
        ["geography_code", "indicator_code", "period"]
    ).any():
        raise ValueError("Duplicate GVA observations found.")

    return output


def transform_north_east_gva() -> pd.DataFrame:
    dataframe = transform_regional_gva()

    return dataframe[
        dataframe["geography_code"] == "TLC"
    ].reset_index(drop=True)


if __name__ == "__main__":
    result = transform_regional_gva()
    print(result.to_string(index=False))