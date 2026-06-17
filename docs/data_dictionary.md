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

## Indicator: `REAL_GVA_GBP_MILLION`

| Attribute | Description |
|---|---|
| Geography | North East; North West |
| Geography codes | `TLC`; `TLD` |
| Frequency | Annual |
| Coverage | 1998–2023 |
| Unit | £ million, chained-volume measures in 2022 prices |
| Source | ONS Regional gross value added balanced by industry |
| Workbook sheet | `Table 1b` |
| Industry coverage | All industries |
| Purpose | Compares the real economic size of the North East and North West over time |

## Labour-market snapshot indicators

| Indicator code | Description |
|---|---|
| `ECONOMIC_ACTIVITY_RATE` | Share of the relevant working-age population that is economically active |
| `EMPLOYMENT_RATE` | Share of the relevant working-age population in employment |
| `UNEMPLOYMENT_RATE` | Share of economically active people who are unemployed |
| `ECONOMIC_INACTIVITY_RATE` | Share of the relevant working-age population that is economically inactive |

### Source metadata

| Attribute | Description |
|---|---|
| Geography | North East; North West |
| Geography codes | `E12000001`; `E12000002` |
| Frequency | Quarterly snapshot |
| Period | January–March 2026 |
| Unit | Percent |
| Source | ONS S01 Regional labour market summary |
| Workbook sheet | `S01.1` |
| Purpose | Compares current regional labour-market conditions across the North East and North West |

## BRES industry employment

The `industry_employment` table stores annual employment counts by region and industry.

| Field | Description |
|---|---|
| `industry_employment_id` | Unique row identifier |
| `geography_id` | Links the observation to the geography table |
| `industry_code` | SIC-based industry code or broad industry group code |
| `industry_name` | Industry description |
| `period` | Observation year |
| `frequency` | Annual |
| `value` | Employment count |
| `unit` | `employment_count` |
| `source_id` | Links the observation to the source table |
| `retrieved_at` | UTC timestamp showing when the data were loaded |

### Source metadata

| Attribute | Description |
|---|---|
| Geography | North East; North West |
| Geography codes | `E12000001`; `E12000002` |
| Coverage | 2015–2024 |
| Frequency | Annual |
| Measure | Employment count |
| Employment status | Employment, including employees and working proprietors |
| Source | Nomis Business Register and Employment Survey, open access |
| Industries | Five broad sectors and twelve detailed green-relevant SIC divisions |
| Purpose | Measures changes in employment across manufacturing, energy, construction, logistics, engineering and research-related industries |

## ASHE regional earnings

The `regional_earnings` table stores annual workplace earnings estimates and their reported confidence percentages.

| Field | Description |
|---|---|
| `regional_earnings_id` | Unique row identifier |
| `geography_id` | Links the observation to the geography table |
| `indicator_code` | Standardised earnings measure |
| `period` | Observation year |
| `frequency` | Annual |
| `value` | Earnings estimate |
| `confidence_pct` | Standard error as a percentage of the estimate |
| `unit` | `gbp_per_week` or `gbp_per_hour` |
| `source_id` | Links the observation to the source table |
| `retrieved_at` | UTC timestamp showing when the data were loaded |

### Indicators

| Indicator code | Description |
|---|---|
| `MEDIAN_WEEKLY_GROSS_PAY` | Median gross weekly pay for full-time workers |
| `MEDIAN_HOURLY_PAY_EXCL_OVERTIME` | Median hourly pay excluding overtime for full-time workers |

### Source metadata

| Attribute | Description |
|---|---|
| Geography | North East; North West |
| Geography codes | `E12000001`; `E12000002` |
| Coverage | 1997 to latest available year |
| Frequency | Annual |
| Population | Full-time workers |
| Statistic | Median |
| Source | Nomis Annual Survey of Hours and Earnings, workplace analysis |
| Purpose | Compares regional wage levels and underlying labour costs over time |