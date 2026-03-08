"""Close-gate verification for HEDIS module."""
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from starguard_core.hedis import (
    predict_closure_batch,
    build_intervention_plan,
    default_hedis_scenario,
)

gaps = default_hedis_scenario()
preds = predict_closure_batch(gaps)
plan = build_intervention_plan(gaps, preds)

assert plan["total_gaps"] == 8, "FAIL: expected 8 gaps"
assert plan["total_revenue_impact_m"] > 0, "FAIL: revenue impact zero"
assert len(plan["demo_narrative"]) > 0, "FAIL: narrative empty"

print("✅ HEDIS module live")
print(f"   Total gaps:      {plan['total_gaps']}")
print(f"   Actionable gaps: {plan['actionable_gaps']}")
print(f"   Star impact:     {plan['total_star_impact']}")
print(f"   Revenue impact:  ${plan['total_revenue_impact_m']:.2f}M")
print(f"   Narrative:       {plan['demo_narrative']}")
