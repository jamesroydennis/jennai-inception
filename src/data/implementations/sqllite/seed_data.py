# /src/data/implementations/sqllite/seed_data.py

import sqlite3
from config.config import DB_PATH

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Insert one product
    cur.execute("INSERT INTO products (name, hs_code, description) VALUES (?, ?, ?)", 
                ("Cotton T-Shirt", "6109.10", "Basic short-sleeve cotton T-shirt"))

    # Insert 4 regions
    regions = [
        ("Vietnam", "VN", "ASEAN"),
        ("Bangladesh", "BD", "SAARC"),
        ("Mexico", "MX", "USMCA"),
        ("Turkey", "TR", "EU Customs")
    ]
    cur.executemany("INSERT INTO regions (name, iso_code, group_name) VALUES (?, ?, ?)", regions)

    # Tariffs
    cur.executemany("""
        INSERT INTO tariff_data (product_id, region_id, tariff_percent, effective_date, source_id)
        VALUES (1, ?, ?, '2025-07-01', 1)
    """, [(1, 5.0), (2, 10.0), (3, 7.5), (4, 6.5)])

    # FX
    cur.executemany("""
        INSERT INTO currency_data (region_id, currency_code, rate_to_usd, volatility, timestamp, source_id)
        VALUES (?, ?, ?, ?, '2025-07-25T00:00:00Z', 1)
    """, [
        (1, "VND", 24000, 0.08),
        (2, "BDT", 110, 0.12),
        (3, "MXN", 18, 0.05),
        (4, "TRY", 32, 0.20)
    ])

    # Supply
    cur.executemany("""
        INSERT INTO supply_data (product_id, region_id, availability_score, avg_shipping_time_days, delay_index, timestamp, source_id)
        VALUES (1, ?, ?, ?, ?, '2025-07-25T00:00:00Z', 1)
    """, [
        (1, 0.9, 12, 0.1),
        (2, 0.85, 16, 0.15),
        (3, 0.8, 7, 0.2),
        (4, 0.75, 10, 0.25)
    ])

    # UQ
    cur.executemany("""
        INSERT INTO risk_signals (region_id, fx_volatility, political_instability, supply_disruption, news_sentiment, calculated_uq, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, '2025-07-25T00:00:00Z')
    """, [
        (1, 0.08, 0.1, 0.1, 0.1, 0.09),
        (2, 0.12, 0.2, 0.2, 0.15, 0.17),
        (3, 0.05, 0.05, 0.05, 0.1, 0.063),
        (4, 0.2, 0.25, 0.3, 0.2, 0.237)
    ])

    conn.commit()
    conn.close()
