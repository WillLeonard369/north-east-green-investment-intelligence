from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from src.ne_investment.transform.regional_gva_levels import (
    transform_regional_gva_levels,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def load_regional_gva_levels() -> None:
    dataframe = transform_regional_gva_levels()
    retrieved_at = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT source_id
            FROM data_sources
            WHERE source_name = ?
              AND dataset_name = ?
            LIMIT 1
            """,
            (
                "ONS Regional GVA",
                "Regional gross value added balanced by industry",
            ),
        )

        source = cursor.fetchone()

        if source is None:
            raise ValueError(
                "ONS source record not found. Run the regional GVA loader first."
            )

        source_id = source[0]

        geography_ids = {
            code: geography_id
            for geography_id, code in cursor.execute(
                """
                SELECT geography_id, geography_code
                FROM geography
                """
            ).fetchall()
        }

        rows = [
            (
                geography_ids[row.geography_code],
                row.indicator_code,
                row.period,
                row.frequency,
                row.value,
                row.unit,
                source_id,
                retrieved_at,
            )
            for row in dataframe.itertuples(index=False)
        ]

        cursor.executemany(
            """
            INSERT OR REPLACE INTO economic_observations (
                geography_id,
                indicator_code,
                period,
                frequency,
                value,
                unit,
                source_id,
                retrieved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

        connection.commit()

    print(
        f"Loaded {len(dataframe)} real GVA level observations "
        f"for {dataframe['geography_code'].nunique()} regions."
    )


if __name__ == "__main__":
    load_regional_gva_levels()