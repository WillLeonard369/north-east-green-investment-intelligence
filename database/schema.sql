PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS data_sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    dataset_name TEXT,
    publisher TEXT,
    source_url TEXT,
    licence TEXT,
    accessed_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS geography (
    geography_id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_code TEXT NOT NULL UNIQUE,
    geography_name TEXT NOT NULL,
    geography_type TEXT NOT NULL,
    parent_code TEXT
);

CREATE TABLE IF NOT EXISTS economic_observations (
    observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_id INTEGER NOT NULL,
    indicator_code TEXT NOT NULL,
    period TEXT NOT NULL,
    frequency TEXT NOT NULL,
    value REAL,
    unit TEXT,
    source_id INTEGER NOT NULL,
    retrieved_at TEXT NOT NULL,

    FOREIGN KEY (geography_id)
        REFERENCES geography(geography_id),

    FOREIGN KEY (source_id)
        REFERENCES data_sources(source_id),

    UNIQUE (
        geography_id,
        indicator_code,
        period,
        source_id
    )
);


CREATE TABLE IF NOT EXISTS industry_employment (
    industry_employment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_id INTEGER NOT NULL,
    industry_code TEXT NOT NULL,
    industry_name TEXT NOT NULL,
    period TEXT NOT NULL,
    frequency TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    source_id INTEGER NOT NULL,
    retrieved_at TEXT NOT NULL,

    FOREIGN KEY (geography_id)
        REFERENCES geography(geography_id),

    FOREIGN KEY (source_id)
        REFERENCES data_sources(source_id),

    UNIQUE (
        geography_id,
        industry_code,
        period,
        source_id
    )
);

CREATE TABLE IF NOT EXISTS regional_earnings (
    regional_earnings_id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_id INTEGER NOT NULL,
    indicator_code TEXT NOT NULL,
    period TEXT NOT NULL,
    frequency TEXT NOT NULL,
    value REAL NOT NULL,
    confidence_pct REAL,
    unit TEXT NOT NULL,
    source_id INTEGER NOT NULL,
    retrieved_at TEXT NOT NULL,

    FOREIGN KEY (geography_id)
        REFERENCES geography(geography_id),

    FOREIGN KEY (source_id)
        REFERENCES data_sources(source_id),

    UNIQUE (
        geography_id,
        indicator_code,
        period,
        source_id
    )
);

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

CREATE TABLE IF NOT EXISTS green_investment_projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    project_type TEXT NOT NULL,
    sector TEXT NOT NULL,
    technology_theme TEXT,
    geography_id INTEGER,
    location_name TEXT,
    developer_name TEXT,
    investor_name TEXT,
    announcement_date TEXT,
    expected_completion_date TEXT,
    project_status TEXT,
    regional_linkage_type TEXT NOT NULL,
regional_linkage_strength TEXT NOT NULL,
total_project_value_gbp REAL,
regional_value_gbp REAL,
total_jobs_announced INTEGER,
regional_jobs_announced INTEGER,
    capacity_value REAL,
    capacity_unit TEXT,
    source_id INTEGER NOT NULL,
    source_url TEXT,
    retrieved_at TEXT NOT NULL,
    notes TEXT,

    FOREIGN KEY (geography_id)
        REFERENCES geography(geography_id),

    FOREIGN KEY (source_id)
        REFERENCES data_sources(source_id),

    UNIQUE (
        project_name,
        developer_name,
        announcement_date
    )
);

