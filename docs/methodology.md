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