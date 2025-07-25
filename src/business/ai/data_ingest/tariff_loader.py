# /src/business/ai/data_ingest/tariff_loader.py

import sqlite3
from . import ai_logging_decorator
from config.config import DB_PATH
from core.logging_decorator import LoggingAIDecorator

@LoggingAIDecorator
def load_tariff_data(product_id=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT r.name, td.tariff_percent
    FROM tariff_data td
    JOIN regions r ON td.region_id = r.id
    WHERE td.product_id = ?
    """
    cursor.execute(query, (product_id,))
    rows = cursor.fetchall()
    conn.close()

    # Output as dict: { 'Vietnam': 8.5, 'Egypt': 5.0, ... }
    return {region: tariff for region, tariff in rows}

if __name__ == "__main__":
    print(load_tariff_data())
