# /src/business/ai/data_ingest/fx_loader.py

import sqlite3
from config.config import DB_PATH
from core.logging_decorator import LoggingAIDecorator

@LoggingAIDecorator
def load_fx_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT r.name, cd.rate_to_usd, cd.volatility
    FROM currency_data cd
    JOIN regions r ON cd.region_id = r.id
    ORDER BY cd.timestamp DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    fx_data = {}
    for region, rate, vol in rows:
        if region not in fx_data:
            fx_data[region] = {
                "rate_to_usd": rate,
                "volatility": vol
            }

    return fx_data

if __name__ == "__main__":
    fx = load_fx_data()
    for region, data in fx.items():
        print(f"{region}: USD Rate = {data['rate_to_usd']}, Volatility = {data['volatility']}")
