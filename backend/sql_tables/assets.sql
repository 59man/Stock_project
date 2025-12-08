CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    symbol TEXT NOT NULL UNIQUE,
    isin TEXT,
    type TEXT NOT NULL,
    provider TEXT NOT NULL,
    currency TEXT NOT NULL
);