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


def transform_north_east_gva() -> pd.DataFrame:
    dataframe = pd.read_excel(
        SOURCE_FILE,
        sheet_name="Table 1a",
        header=1,
    )

    north_east_total = dataframe[
        (dataframe["ITL code"] == "TLC")
        & (dataframe["SIC07 code"] == "Total")
    ].iloc[0]

    year_columns = [
        column for column in dataframe.columns
        if str(column).isdigit()
    ]

    output = pd.DataFrame(
        {
            "geography_code": "TLC",
            "geography_name": "North East",
            "indicator_code": "REAL_GVA_INDEX",
            "period": [str(year) for year in year_columns],
            "frequency": "annual",
            "value": [north_east_total[year] for year in year_columns],
            "unit": "index_2022_100",
        }
    )

    output["value"] = pd.to_numeric(output["value"], errors="coerce")

    if output["value"].isna().any():
        raise ValueError("Missing or invalid GVA values found.")

    if output.duplicated(
        ["geography_code", "indicator_code", "period"]
    ).any():
        raise ValueError("Duplicate GVA observations found.")

    return output


if __name__ == "__main__":
    result = transform_north_east_gva()
    print(result.to_string(index=False))