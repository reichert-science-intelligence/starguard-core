"""Closure prediction — synthetic model for demo. Imports models only."""
from starguard_core.hedis.models import ClosurePrediction, HedisGap

# Closure probability by star_impact (higher impact -> lower baseline closure)
_STAR_TO_BASELINE: dict[int, float] = {
    1: 0.75,
    2: 0.65,
    3: 0.55,
    4: 0.45,
    5: 0.35,
}


def predict_closure_batch(gaps: list[HedisGap]) -> list[ClosurePrediction]:
    """Predict closure probability for each gap. Returns one prediction per gap."""
    preds: list[ClosurePrediction] = []
    for g in gaps:
        base = _STAR_TO_BASELINE.get(g.star_impact, 0.5)
        # Slight variation by gap_id hash for demo variety
        var = (hash(g.gap_id) % 20) / 100.0 - 0.1
        prob = max(0.1, min(0.95, base + var))
        intervention = "Outreach" if prob < 0.5 else "Clinical"
        preds.append(
            ClosurePrediction(
                gap_id=g.gap_id,
                closure_probability=round(prob, 4),
                recommended_intervention=intervention,
            )
        )
    return preds
