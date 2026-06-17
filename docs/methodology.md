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

## ASHE regional earnings extension

The project includes annual regional earnings data from the Nomis Annual Survey of Hours and Earnings workplace analysis.

The transformation script:

```text
src/ne_investment/transform/ashe_earnings.py

performs the following steps:

reads the Nomis ASHE workbook;
selects full-time workers;
extracts the median weekly gross pay series;
extracts the median hourly pay excluding overtime series;
records North East and North West values separately;
preserves the reported confidence percentage for each estimate;
converts the data into long format;
validates missing values and duplicate region-indicator-year combinations.

The loader script:

src/ne_investment/load/ashe_earnings.py

stores the data in the regional_earnings table.

The resulting SQL view:

regional_earnings_view

supports comparison of wage levels and labour costs between the North East and North West over time.

ASHE estimates are survey-based and should be interpreted alongside the reported confidence percentages, particularly when comparing smaller year-to-year movements.

## Green investment projects extension

The project includes a manually verified database of major clean-energy and advanced-manufacturing investments connected to North East England.

The source file:

```text
data/reference/green_projects/project_template.csv

stores one row per project and records:

project type and technology theme;
location;
developer and investor;
announcement and completion dates;
project status;
total project value and jobs;
North East-attributable value and jobs;
capacity;
source details;
attribution notes.

The transformation script:

src/ne_investment/transform/green_projects.py

performs the following steps:

checks that all required columns are present;
converts investment, jobs and capacity fields to numeric values;
standardises date fields;
validates required project and source information;
restricts regional-linkage strength to direct, significant or indirect;
checks for duplicate project records.

The loader script:

src/ne_investment/load/green_projects.py

stores the verified records in the green_investment_projects table.

The resulting SQL view:

green_investment_projects_view

supports analysis of project location, technology, investment, employment and regional linkage.

Regional attribution methodology

Projects are not automatically treated as wholly attributable to the North East.

Each record distinguishes between:

total_project_value_gbp and regional_value_gbp;
total_jobs_announced and regional_jobs_announced;
the type of regional connection;
the strength of that connection.

A project receives a direct classification where the investment facility or principal project site is physically located in the region.

A significant classification is used where the project has a major regional operations, port, grid or supply-chain connection but is not wholly located in the region.

An indirect classification is used where the regional connection is limited or secondary.

Regional investment and employment values are populated only when reliable sources explicitly support local attribution. Where only the overall project value is available, the regional fields remain blank rather than assuming the full value belongs to the North East.

Current verified records

The database currently includes:

SeAH Wind’s offshore-wind monopile manufacturing facility at Teesworks;
JDR Cable Systems’ subsea cable manufacturing facility at Cambois.

Both are classified as direct North East manufacturing investments.