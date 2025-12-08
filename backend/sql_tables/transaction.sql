CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    asset_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    bought_at TEXT NOT NULL,
    price REAL,
    FOREIGN KEY(asset_id) REFERENCES assets(id)
);
