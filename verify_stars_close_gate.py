"""Close-gate verification for Stars module."""
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from starguard_core.stars import (
    default_stars_scenario,
    compute_bonus_threshold_impact,
    project_stars,
)

profiles = default_stars_scenario()
assert len(profiles) == 3, "FAIL: expected 3 profiles"

moderate = profiles[1]
impact = compute_bonus_threshold_impact(moderate)

assert "baseline_stars" in impact
assert "projected_stars" in impact
assert "crosses_qbp_threshold" in impact
assert "qbp_revenue_at_4_0_m" in impact
assert len(impact["demo_narrative"]) > 0

print("[OK] Stars module live")
print(f"   Profiles:       {len(profiles)} (Low 4.5, Moderate 3.5, High 2.5)")
print(f"   Moderate:       {moderate.baseline_stars} -> {project_stars(moderate)} stars")
print(f"   Crosses QBP:    {impact['crosses_qbp_threshold']}")
print(f"   QBP at 4.0:     ${impact['qbp_revenue_at_4_0_m']:.1f}M (50K members)")
print(f"   Narrative:      {impact['demo_narrative'][:80]}...")
