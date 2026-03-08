"""Intervention planning — actionable gaps and revenue impact. Imports models only."""
from starguard_core.hedis.models import ClosurePrediction, HedisGap

# Actionable = closure probability below threshold
ACTIONABLE_THRESHOLD: float = 0.6


def build_intervention_plan(
    gaps: list[HedisGap], preds: list[ClosurePrediction]
) -> dict[str, int | float | str]:
    """Build intervention plan from gaps and predictions. Produces demo_narrative."""
    pred_by_id = {p.gap_id: p for p in preds}
    actionable = 0
    total_star = 0
    total_revenue = 0.0
    for g in gaps:
        p = pred_by_id.get(g.gap_id)
        if p and p.closure_probability < ACTIONABLE_THRESHOLD:
            actionable += 1
        total_star += g.star_impact
        total_revenue += g.roi_estimate
    total_revenue_m = total_revenue / 1_000_000.0
    demo_narrative = (
        f"{len(gaps)} gaps, {actionable} actionable → "
        f"${total_revenue_m:.2f}M revenue impact, {total_star} star points"
    )
    return {
        "total_gaps": len(gaps),
        "actionable_gaps": actionable,
        "total_star_impact": total_star,
        "total_revenue_impact_m": round(total_revenue_m, 2),
        "demo_narrative": demo_narrative,
    }
