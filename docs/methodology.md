# Methodology

## Overview

The project uses a reproducible extract-transform-load process to collect, clean, validate and store regional economic data for North East England.

## Data pipeline

### 1. Extract

The original ONS Excel workbook is downloaded manually and stored locally in:

```text
data/raw/ons/

Raw files are kept unchanged so the source data remain auditable.

2. Transform

The Python transformation script:

src/ne_investment/transform/ons_gva.py

performs the following steps:

reads Table 1a from the ONS workbook;
identifies the North East using ITL code TLC;
selects the all-industries total;
converts year columns into a long-format time series;
assigns standardised indicator labels;
converts values to numeric format;
checks for missing and duplicate observations.
3. Load

The loader script:

src/ne_investment/load/ons_gva.py

inserts the transformed data into the SQLite database.

The database records:

source metadata;
geography metadata;
annual economic observations;
retrieval timestamps.
4. Analyse

The analysis script:

src/ne_investment/analysis/gva_analysis.py

queries the SQL view and calculates annual percentage changes in the GVA index.

5. Validate

Automated tests check that:

the dataset is not empty;
all observations relate to the North East;
indicator codes are consistent;
values are not missing;
years are correctly ordered;
annual growth rates are calculated successfully.

Future development will add:

industry-level GVA;
employment and productivity indicators;
additional UK regions for comparison;
company-level and transaction data;
green investment and project data.

## Subregional manufacturing extension

The project also includes a separate pipeline for manufacturing GVA at ITL2 level.

The transformation script:

```text
src/ne_investment/transform/subregional_manufacturing.py

performs the following steps:

reads Table 2a from the ONS workbook;
filters for Tees Valley (TLC3);
filters for Northumberland, Durham and Tyne & Wear (TLC4);
selects the manufacturing industry;
converts annual columns into long format;
assigns the indicator code MANUFACTURING_GVA_INDEX;
validates missing values and duplicates.

## Regional labour-market snapshot extension

The project includes a current labour-market comparison for the North East and North West using the ONS S01 Regional labour market summary.

The transformation script:

```text
src/ne_investment/transform/regional_labour_market_snapshot.py

performs the following steps:

reads the S01.1 worksheet from the ONS labour-market workbook;
identifies the North East (E12000001) and North West (E12000002);
keeps the first headline row for each region;
extracts economic activity, employment, unemployment and economic inactivity rates;
assigns standardised internal indicator codes;
records the period as 2026-Q1;
validates missing values and duplicate observations.

The loader script:

src/ne_investment/load/regional_labour_market_snapshot.py

stores the eight labour-market observations in the SQLite database.

The resulting SQL view:

regional_labour_market_snapshot

supports comparison of current labour-market conditions between the two regions.

This is currently a snapshot rather than a historical time series. A later stage will add comparable observations across multiple periods.

The loader script:

src/ne_investment/load/subregional_manufacturing.py

stores both subregional series in the SQLite database.

The resulting SQL view:

subregional_manufacturing_gva

supports comparison of manufacturing output trends across the two North East ITL2 areas.

## Regional real GVA levels extension

The project also includes a pipeline for comparing the actual economic size of the North East and North West.

The transformation script:

```text
src/ne_investment/transform/regional_gva_levels.py

performs the following steps:

reads Table 1b from the ONS workbook;
filters for the North East (TLC) and North West (TLD);
selects the all-industries total;
converts annual columns into long format;
assigns the indicator code REAL_GVA_GBP_MILLION;
records values in £ million using chained-volume measures at 2022 prices;
validates missing values and duplicates.

The loader script:

src/ne_investment/load/regional_gva_levels.py

stores the two regional series in the SQLite database.

The resulting SQL view:

regional_gva_levels

supports comparison of the absolute real GVA levels of the two regional economies over time.

## BRES industry-employment extension

The project includes annual industry-employment data from the Nomis Business Register and Employment Survey open-access dataset.

The transformation script:

```text
src/ne_investment/transform/bres_employment.py

performs the following steps:

reads the Nomis BRES workbook;
selects the Employment blocks for the North East and North West;
excludes the narrower Employees blocks;
extracts annual observations from 2015 to 2024;
separates industry codes from industry descriptions;
reshapes the data into long format;
validates missing values and duplicate region-industry-year combinations.

The selected industries include five broad sectors and twelve detailed divisions relevant to the green and advanced-manufacturing economy, including:

manufacturing;
construction;
transport and storage;
professional, scientific and technical activities;
basic metals;
fabricated metal products;
electrical equipment;
machinery and equipment;
motor vehicles;
other transport equipment;
electricity and gas supply;
civil engineering;
warehousing and transport support;
architectural and engineering activities;
scientific research and development.

The loader script:

src/ne_investment/load/bres_employment.py

stores the data in the industry_employment table.

The resulting SQL view:

bres_industry_employment

supports analysis of regional employment trends by sector and detailed industry.

BRES provides point-in-time workplace employment estimates. ONS notes that it is not primarily designed as a continuous time-series dataset, so results should be interpreted carefully when comparing year-to-year changes.