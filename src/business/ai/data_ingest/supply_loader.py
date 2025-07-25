# /src/business/ai/data_ingest/supply_loader.py

import sqlite3
from config.config import DB_PATH
from core.logging_decorator import LoggingAIDecorator

@LoggingAIDecorator
def load_supply_data(product_id=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT r.name, sd.availability_score, sd.avg_shipping_time_days, sd.delay_index
    FROM supply_data sd
    JOIN regions r ON sd.region_id = r.id
    WHERE sd.product_id = ?
    ORDER BY sd.timestamp DESC
    """
    cursor.execute(query, (product_id,))
    rows = cursor.fetchall()
    conn.close()

    supply_data = {}
    for region, availability, shipping_time, delay in rows:
        if region not in supply_data:
            supply_data[region] = {
                "availability_score": availability,
                "avg_shipping_time_days": shipping_time,
                "delay_index": delay
            }

    return supply_data

if __name__ == "__main__":
    data = load_supply_data()
    for region, metrics in data.items():
        print(f"{region}: {metrics}")
