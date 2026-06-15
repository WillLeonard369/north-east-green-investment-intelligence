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