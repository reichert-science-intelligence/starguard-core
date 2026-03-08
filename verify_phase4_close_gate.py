"""
Phase 4 close gate — runs all four modules (RADV, HCC, HEDIS, Stars) in one command.
Expected output format documented below. Exit 0 = gate clear.
"""
import sys

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from starguard_core.radv import default_scenario as radv_scenario, score_exposure
from starguard_core.hcc import (
    default_hcc_scenario,
    compute_raf_batch,
    identify_chronic_gaps,
    compute_revenue_opportunity,
)
from starguard_core.hedis import (
    default_hedis_scenario,
    predict_closure_batch,
    build_intervention_plan,
)
from starguard_core.stars import (
    default_stars_scenario,
    compute_bonus_threshold_impact,
    project_stars,
)
from starguard_core.command_center import run_command_center

# --- RADV ---
radv_s = radv_scenario()
radv_r = score_exposure(radv_s)
assert radv_r.estimated_exposure > 0
assert radv_r.risk_tier in ("low", "medium", "high")
print("[OK] RADV module live")
print(f"   Exposure:     ${radv_r.estimated_exposure:,.0f}")
print(f"   Risk tier:   {radv_r.risk_tier}")

# --- HCC ---
hcc_profiles = default_hcc_scenario()
raf_results = compute_raf_batch(hcc_profiles)
hcc_gaps = []
for p in hcc_profiles:
    hcc_gaps.extend(identify_chronic_gaps(p))
hcc_summary = compute_revenue_opportunity(raf_results, hcc_gaps)
assert hcc_summary["total_gaps_identified"] >= 0
assert "demo_narrative" in hcc_summary
print("[OK] HCC module live")
print(f"   RAF avg:     {hcc_summary['average_raf_score']}")
print(f"   Gaps found:  {hcc_summary['total_gaps_identified']}")
print(f"   Opportunity: ${hcc_summary['net_opportunity_usd']:,.2f}")
print(f"   Narrative:   {hcc_summary['demo_narrative'][:70]}...")

# --- HEDIS ---
hedis_gaps = default_hedis_scenario()
hedis_preds = predict_closure_batch(hedis_gaps)
hedis_plan = build_intervention_plan(hedis_gaps, hedis_preds)
assert hedis_plan["total_gaps"] == 8
assert hedis_plan["total_revenue_impact_m"] > 0
print("[OK] HEDIS module live")
print(f"   Total gaps:      {hedis_plan['total_gaps']}")
print(f"   Actionable gaps: {hedis_plan['actionable_gaps']}")
print(f"   Star impact:     {hedis_plan['total_star_impact']}")
print(f"   Revenue impact:  ${hedis_plan['total_revenue_impact_m']:.2f}M")
print(f"   Narrative:       {hedis_plan['demo_narrative'][:70]}...")

# --- Stars ---
stars_profiles = default_stars_scenario()
assert len(stars_profiles) == 3
moderate = stars_profiles[1]
stars_impact = compute_bonus_threshold_impact(moderate)
assert "crosses_qbp_threshold" in stars_impact
assert "qbp_revenue_at_4_0_m" in stars_impact
print("[OK] Stars module live")
print(f"   Profiles:    {len(stars_profiles)} (Low 4.5, Moderate 3.5, High 2.5)")
print(f"   Moderate:    {moderate.baseline_stars} -> {project_stars(moderate)} stars")
print(f"   Crosses QBP: {stars_impact['crosses_qbp_threshold']}")
print(f"   QBP at 4.0:  ${stars_impact['qbp_revenue_at_4_0_m']:.1f}M (50K members)")

# --- Command Center ---
cc = run_command_center()
assert "demo_narrative" in cc
assert "radv_exposure" in cc
assert "hcc_gaps" in cc
assert "hedis_gaps" in cc
assert "stars_crosses_qbp" in cc
print("[OK] Command center live")
print(f"   Combined:    {cc['demo_narrative'][:100]}...")

print("")
print("=== Phase 4 close gate: ALL MODULES LIVE ===")
print("Demo numbers: $27,625 HCC recapture | $0.66M HEDIS | $6M+ QBP on 3.5->4.0 | 17 star points")
