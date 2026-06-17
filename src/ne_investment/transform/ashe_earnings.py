from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "nomis"
    / "ashe"
    / "nomis_2026_06_17_141323.xlsx"
)

REGIONS = {
    "E12000001": {
        "name": "North East",
        "value_column": 1,
        "confidence_column": 2,
    },
    "E12000002": {
        "name": "North West",
        "value_column": 3,
        "confidence_column": 4,
    },
}

MEASURE_BLOCKS = {
    "MEDIAN_WEEKLY_GROSS_PAY": {
        "start_row": 10,
        "end_row": 44,
        "unit": "gbp_per_week",
    },
    "MEDIAN_HOURLY_PAY_EXCL_OVERTIME": {
        "start_row": 54,
        "end_row": None,
        "unit": "gbp_per_hour",
    },
}


def transform_ashe_earnings() -> pd.DataFrame:
    raw = pd.read_excel(
        SOURCE_FILE,
        sheet_name="Data",
        header=None,
    )

    output_rows = []

    for indicator_code, block_metadata in MEASURE_BLOCKS.items():
        block = raw.iloc[
            block_metadata["start_row"]:block_metadata["end_row"]
        ].copy()

        block = block[
            block[0]
            .astype(str)
            .str.match(r"^\d{4}$", na=False)
        ].copy()

        for geography_code, region_metadata in REGIONS.items():
            for _, row in block.iterrows():
                output_rows.append(
                    {
                        "geography_code": geography_code,
                        "geography_name": region_metadata["name"],
                        "indicator_code": indicator_code,
                        "period": str(int(row.iloc[0])),
                        "frequency": "annual",
                        "value": row.iloc[
                            region_metadata["value_column"]
                        ],
                        "confidence_pct": row.iloc[
                            region_metadata["confidence_column"]
                        ],
                        "unit": block_metadata["unit"],
                    }
                )

    output = pd.DataFrame(output_rows)

    output["value"] = pd.to_numeric(
        output["value"],
        errors="coerce",
    )

    output["confidence_pct"] = pd.to_numeric(
        output["confidence_pct"],
        errors="coerce",
    )

    if output.empty:
        raise ValueError("No ASHE earnings observations found.")

    if output["value"].isna().any():
        raise ValueError("Missing or invalid ASHE earnings values found.")

    if output.duplicated(
        [
            "geography_code",
            "indicator_code",
            "period",
        ]
    ).any():
        raise ValueError("Duplicate ASHE earnings observations found.")

    return output


if __name__ == "__main__":
    result = transform_ashe_earnings()
    print(result.head(20).to_string(index=False))
    print(f"\nRows: {len(result)}")