from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "nomis"
    / "bres"
    / "nomis_2026_06_17_133539.xlsx"
)

REGION_BLOCKS = {
    "E12000001": {
        "name": "North East",
        "start_row": 42,
        "end_row": 59,
    },
    "E12000002": {
        "name": "North West",
        "start_row": 106,
        "end_row": 123,
    },
}


def transform_bres_employment() -> pd.DataFrame:
    raw = pd.read_excel(
        SOURCE_FILE,
        sheet_name="Data",
        header=None,
    )

    year_columns = {
        1: "2015",
        3: "2016",
        5: "2017",
        7: "2018",
        9: "2019",
        11: "2020",
        13: "2021",
        15: "2022",
        17: "2023",
        19: "2024",
    }

    output_rows = []

    for geography_code, metadata in REGION_BLOCKS.items():
        block = raw.iloc[
            metadata["start_row"]:metadata["end_row"]
        ].copy()

        for _, row in block.iterrows():
            industry_raw = str(row.iloc[0]).strip()

            if " : " not in industry_raw:
                continue

            industry_code, industry_name = industry_raw.split(
                " : ",
                maxsplit=1,
            )

            for column_index, year in year_columns.items():
                output_rows.append(
                    {
                        "geography_code": geography_code,
                        "geography_name": metadata["name"],
                        "industry_code": industry_code.strip(),
                        "industry_name": industry_name.strip(),
                        "period": year,
                        "frequency": "annual",
                        "value": row.iloc[column_index],
                        "unit": "employment_count",
                    }
                )

    output = pd.DataFrame(output_rows)
    output["value"] = pd.to_numeric(
        output["value"],
        errors="coerce",
    )

    if output.empty:
        raise ValueError("No BRES employment observations found.")

    if output["value"].isna().any():
        raise ValueError(
            "Missing or invalid BRES employment values found."
        )

    if output.duplicated(
        [
            "geography_code",
            "industry_code",
            "period",
        ]
    ).any():
        raise ValueError(
            "Duplicate BRES employment observations found."
        )

    return output


if __name__ == "__main__":
    result = transform_bres_employment()
    print(result.head(30).to_string(index=False))
    print(f"\nRows: {len(result)}")