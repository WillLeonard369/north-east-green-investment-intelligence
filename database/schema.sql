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

