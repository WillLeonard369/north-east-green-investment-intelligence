CREATE VIEW IF NOT EXISTS regional_gva AS
SELECT
    g.geography_code,
    g.geography_name,
    e.indicator_code,
    e.period,
    e.value,
    e.unit,
    e.frequency
FROM economic_observations AS e
JOIN geography AS g
    ON e.geography_id = g.geography_id
WHERE e.indicator_code = 'REAL_GVA_INDEX';

CREATE VIEW IF NOT EXISTS north_east_gva AS
SELECT *
FROM regional_gva
WHERE geography_code = 'TLC';

CREATE VIEW IF NOT EXISTS subregional_manufacturing_gva AS
SELECT
    g.geography_code,
    g.geography_name,
    e.indicator_code,
    e.period,
    e.value,
    e.unit,
    e.frequency
FROM economic_observations AS e
JOIN geography AS g
    ON e.geography_id = g.geography_id
WHERE e.indicator_code = 'MANUFACTURING_GVA_INDEX';

CREATE VIEW IF NOT EXISTS regional_gva_levels AS
SELECT
    g.geography_code,
    g.geography_name,
    e.indicator_code,
    e.period,
    e.value,
    e.unit,
    e.frequency
FROM economic_observations AS e
JOIN geography AS g
    ON e.geography_id = g.geography_id
WHERE e.indicator_code = 'REAL_GVA_GBP_MILLION';

CREATE VIEW IF NOT EXISTS regional_labour_market_snapshot AS
SELECT
    g.geography_code,
    g.geography_name,
    e.indicator_code,
    e.period,
    e.value,
    e.unit,
    e.frequency
FROM economic_observations AS e
JOIN geography AS g
    ON e.geography_id = g.geography_id
WHERE e.indicator_code IN (
    'ECONOMIC_ACTIVITY_RATE',
    'EMPLOYMENT_RATE',
    'UNEMPLOYMENT_RATE',
    'ECONOMIC_INACTIVITY_RATE'
);

CREATE VIEW IF NOT EXISTS historical_regional_labour_market AS
SELECT
    g.geography_code,
    g.geography_name,
    e.indicator_code,
    e.period,
    e.value,
    e.unit,
    e.frequency
FROM economic_observations AS e
JOIN geography AS g
    ON e.geography_id = g.geography_id
WHERE e.frequency = 'rolling_3_month'
  AND e.indicator_code IN (
      'ECONOMIC_ACTIVITY_RATE',
      'EMPLOYMENT_RATE',
      'UNEMPLOYMENT_RATE',
      'ECONOMIC_INACTIVITY_RATE'
  );

  CREATE VIEW IF NOT EXISTS bres_industry_employment AS
SELECT
    g.geography_code,
    g.geography_name,
    ie.industry_code,
    ie.industry_name,
    ie.period,
    ie.value,
    ie.unit,
    ie.frequency
FROM industry_employment AS ie
JOIN geography AS g
    ON ie.geography_id = g.geography_id;

CREATE VIEW IF NOT EXISTS regional_earnings_view AS
SELECT
    g.geography_code,
    g.geography_name,
    re.indicator_code,
    re.period,
    re.value,
    re.confidence_pct,
    re.unit,
    re.frequency
FROM regional_earnings AS re
JOIN geography AS g
    ON re.geography_id = g.geography_id;

    CREATE VIEW IF NOT EXISTS green_investment_projects_view AS
SELECT
    gip.project_id,
    gip.project_name,
    gip.project_type,
    gip.sector,
    gip.technology_theme,
    g.geography_code,
    g.geography_name,
    gip.location_name,
    gip.developer_name,
    gip.investor_name,
    gip.announcement_date,
    gip.expected_completion_date,
    gip.project_status,
    gip.announced_value_gbp,
    gip.jobs_announced,
    gip.capacity_value,
    gip.capacity_unit,
    gip.source_url,
    gip.notes
FROM green_investment_projects AS gip
LEFT JOIN geography AS g
    ON gip.geography_id = g.geography_id;