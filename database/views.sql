CREATE VIEW IF NOT EXISTS north_east_gva AS
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
WHERE g.geography_code = 'TLC'
  AND e.indicator_code = 'REAL_GVA_INDEX';