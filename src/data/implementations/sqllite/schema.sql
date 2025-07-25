# save_schema.py — place this wherever you want to run it from (e.g. scripts/tools)

from config.config import DATA_DIR
from pathlib import Path

schema_sql = """
-- Schema for Global Textile Arbitrage System

-- Source metadata
CREATE TABLE sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT,
    url TEXT,
    last_updated TIMESTAMP
);

-- Regions and trade groups
CREATE TABLE regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    iso_code TEXT,
    group_name TEXT
);

-- Products (SKUs)
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hs_code TEXT,
    description TEXT
);

-- Tariff data
CREATE TABLE tariff_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    region_id INTEGER,
    tariff_percent REAL,
    effective_date DATE,
    source_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (region_id) REFERENCES regions(id),
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

-- Currency and FX data
CREATE TABLE currency_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER,
    currency_code TEXT,
    rate_to_usd REAL,
    volatility REAL,
    timestamp TIMESTAMP,
    source_id INTEGER,
    FOREIGN KEY (region_id) REFERENCES regions(id),
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

-- Supply metrics
CREATE TABLE supply_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    region_id INTEGER,
    availability_score REAL,
    avg_shipping_time_days REAL,
    delay_index REAL,
    timestamp TIMESTAMP,
    source_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (region_id) REFERENCES regions(id),
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

-- Risk signals for unpredictability quotient
CREATE TABLE risk_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER,
    fx_volatility REAL,
    political_instability REAL,
    supply_disruption REAL,
    news_sentiment REAL,
    calculated_uq REAL,
    timestamp TIMESTAMP,
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

-- Final scoring table
CREATE TABLE sourcing_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    region_id INTEGER,
    policy_score REAL,
    currency_score REAL,
    supply_score REAL,
    uq REAL,
    final_score REAL,
    timestamp TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (region_id) REFERENCES regions(id)
);
"""

# Save the schema using the config-defined path
schema_path = DATA_DIR / "schema.sql"
schema_path.parent.mkdir(parents=True, exist_ok=True)

with open(schema_path, "w", encoding="utf-8") as f:
    f.write(schema_sql)

print(f"✅ Schema saved to: {schema_path}")
