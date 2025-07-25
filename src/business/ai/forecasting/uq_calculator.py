# /src/business/ai/forecasting/uq_calculator.py

import sqlite3
from config.config import DB_PATH
from core.logging_decorator import LoggingAIDecorator

@LoggingAIDecorator
def calculate_uq_weights():
    return {
        "fx_volatility": 0.3,
        "political_instability": 0.3,
        "supply_disruption": 0.2,
        "news_sentiment": 0.2
    }

@ai_log_call
def load_uq_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT r.name, rs.fx_volatility, rs.political_instability,
           rs.supply_disruption, rs.news_sentiment
    FROM risk_signals rs
    JOIN regions r ON rs.region_id = r.id
    ORDER BY rs.timestamp DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    weights = calculate_uq_weights()
    uq_data = {}

    for row in rows:
        region = row[0]
        if region not in uq_data:
            fx_vol, pol_instab, supply_disr, news_sent = row[1:]
            uq = (
                weights["fx_volatility"] * fx_vol +
                weights["political_instability"] * pol_instab +
                weights["supply_disruption"] * supply_disr +
                weights["news_sentiment"] * news_sent
            )
            uq_data[region] = round(uq, 4)

    return uq_data

if __name__ == "__main__":
    uq = load_uq_data()
    for region, score in uq.items():
        print(f"{region}: UQ = {score}")
