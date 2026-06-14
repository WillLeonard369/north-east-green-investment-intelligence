# Data Dictionary

## `economic_observations`

Stores regional economic indicators in long format.

| Field | Type | Description |
|---|---|---|
| `observation_id` | Integer | Unique row identifier |
| `geography_id` | Integer | Links the observation to the geography table |
| `indicator_code` | Text | Standardised internal indicator name |
| `period` | Text | Observation year |
| `frequency` | Text | Data frequency, currently annual |
| `value` | Real | Numeric observation value |
| `unit` | Text | Unit of measurement |
| `source_id` | Integer | Links the observation to the source table |
| `retrieved_at` | Text | UTC timestamp showing when the data were loaded |

## Indicator: `REAL_GVA_INDEX`

| Attribute | Description |
|---|---|
| Geography | North East England |
| Geography code | `TLC` |
| Frequency | Annual |
| Coverage | 1998–2023 |
| Unit | Chained-volume-measures index, 2022 = 100 |
| Source | ONS Regional gross value added balanced by industry |
| Workbook sheet | `Table 1a` |
| Industry coverage | All industries |
| Purpose | Measures changes in the volume of regional economic output over time |


## Indicator: `MANUFACTURING_GVA_INDEX`

| Attribute | Description |
|---|---|
| Geography | Tees Valley; Northumberland, Durham and Tyne & Wear |
| Geography codes | `TLC3`; `TLC4` |
| Frequency | Annual |
| Coverage | 1998–2023 |
| Unit | Chained-volume-measures index, 2022 = 100 |
| Source | ONS Regional gross value added balanced by industry |
| Workbook sheet | `Table 2a` |
| Industry coverage | Manufacturing |
| Purpose | Compares changes in manufacturing output across the two North East ITL2 subregions |