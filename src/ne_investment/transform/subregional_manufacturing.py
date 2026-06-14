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

SUBREGIONS = {
    "TLC3": "Tees Valley",
    "TLC4": "Northumberland, Durham and Tyne & Wear",
}


def transform_subregional_manufacturing() -> pd.DataFrame:
    dataframe = pd.read_excel(
        SOURCE_FILE,
        sheet_name="Table 2a",
        header=1,
    )

    manufacturing = dataframe[
        dataframe["ITL code"].isin(SUBREGIONS)
        & (dataframe["SIC07 description"] == "Manufacturing")
    ].copy()

    year_columns = [
        column
        for column in dataframe.columns
        if str(column).isdigit()
    ]

    output_rows = []

    for _, row in manufacturing.iterrows():
        geography_code = row["ITL code"]

        for year in year_columns:
            output_rows.append(
                {
                    "geography_code": geography_code,
                    "geography_name": SUBREGIONS[geography_code],
                    "indicator_code": "MANUFACTURING_GVA_INDEX",
                    "period": str(year),
                    "frequency": "annual",
                    "value": row[year],
                    "unit": "index_2022_100",
                }
            )

    output = pd.DataFrame(output_rows)
    output["value"] = pd.to_numeric(output["value"], errors="coerce")

    if output["value"].isna().any():
        raise ValueError("Missing or invalid manufacturing GVA values found.")

    if output.duplicated(
        ["geography_code", "indicator_code", "period"]
    ).any():
        raise ValueError("Duplicate manufacturing observations found.")

    return output


if __name__ == "__main__":
    result = transform_subregional_manufacturing()
    print(result.to_string(index=False))