"""
Four-module command center — RADV + HCC + HEDIS + Stars compound narrative.
Maps directly to 2:30 demo script.
"""
from starguard_core.radv import default_scenario, score_exposure
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
)


def run_command_center() -> dict[str, str | float | int]:
    """
    Wire RADV + HCC + HEDIS + Stars into a single compound narrative.
    Returns dict with module summaries and combined demo_narrative.
    """
    # RADV
    radv_scenario = default_scenario()
    radv_result = score_exposure(radv_scenario)
    radv_narrative = f"RADV exposure ${radv_result.estimated_exposure:,.0f} ({radv_result.risk_tier} risk)"

    # HCC
    hcc_profiles = default_hcc_scenario()
    raf_results = compute_raf_batch(hcc_profiles)
    hcc_gaps = []
    for p in hcc_profiles:
        hcc_gaps.extend(identify_chronic_gaps(p))
    hcc_summary = compute_revenue_opportunity(raf_results, hcc_gaps)
    hcc_narrative = hcc_summary["demo_narrative"]

    # HEDIS
    hedis_gaps = default_hedis_scenario()
    hedis_preds = predict_closure_batch(hedis_gaps)
    hedis_plan = build_intervention_plan(hedis_gaps, hedis_preds)
    hedis_narrative = hedis_plan["demo_narrative"]

    # Stars
    stars_profiles = default_stars_scenario()
    stars_impact = compute_bonus_threshold_impact(stars_profiles[1])  # Moderate profile
    stars_narrative = stars_impact["demo_narrative"]

    combined = (
        f"Command Center: {radv_narrative} | "
        f"HCC: {hcc_narrative} | "
        f"HEDIS: {hedis_narrative} | "
        f"Stars: {stars_narrative}"
    )
    return {
        "radv_narrative": radv_narrative,
        "hcc_narrative": hcc_narrative,
        "hedis_narrative": hedis_narrative,
        "stars_narrative": stars_narrative,
        "demo_narrative": combined,
        "radv_exposure": radv_result.estimated_exposure,
        "hcc_gaps": hcc_summary["total_gaps_identified"],
        "hedis_gaps": hedis_plan["total_gaps"],
        "hedis_revenue_m": hedis_plan["total_revenue_impact_m"],
        "stars_crosses_qbp": stars_impact["crosses_qbp_threshold"],
    }
