# /src/business/ai/pricing_engine/scorer.py

from data_ingest.tariff_loader import load_tariff_data
from data_ingest.fx_loader import load_fx_data
from data_ingest.supply_loader import load_supply_data
from forecasting.uq_calculator import load_uq_data
from core.logging_decorator import LoggingAIDecorator

@LoggingAIDecorator
def score_regions(product_id=1):
    # Load raw data
    tariffs = load_tariff_data(product_id)
    fx = load_fx_data()
    supply = load_supply_data(product_id)
    uq = load_uq_data()

    # Set weights
    weights = {
        "policy": 0.4,
        "currency": 0.3,
        "supply": 0.3
    }

    # Normalize + score
    scores = {}

    for region in tariffs:
        if region not in fx or region not in supply or region not in uq:
            continue

        # Invert tariff (lower is better)
        policy_score = 1 - min(tariffs[region] / 100, 1.0)

        # Currency: we want stable, strong exchange + low volatility
        fx_score = 1 - fx[region]["volatility"]

        # Supply: weighted average (could get fancier later)
        supply_score = (
            0.5 * supply[region]["availability_score"] +
            0.3 * (1 - (supply[region]["delay_index"])) +
            0.2 * (1 - (supply[region]["avg_shipping_time_days"] / 30))  # assume 30 days max baseline
        )

        uq_score = uq[region]
        raw_score = (
            weights["policy"] * policy_score +
            weights["currency"] * fx_score +
            weights["supply"] * supply_score
        )

        final_score = round(raw_score * (1 - uq_score), 4)
        scores[region] = {
            "policy_score": round(policy_score, 4),
            "currency_score": round(fx_score, 4),
            "supply_score": round(supply_score, 4),
            "uq": round(uq_score, 4),
            "final_score": final_score
        }

    return dict(sorted(scores.items(), key=lambda x: x[1]["final_score"], reverse=True))

if __name__ == "__main__":
    from pprint import pprint
    pprint(score_regions())
