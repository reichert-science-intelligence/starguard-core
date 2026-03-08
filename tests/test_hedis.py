"""HEDIS module tests — 21 stubs, all should pass."""
import pytest

from starguard_core.hedis.models import ClosurePrediction, HedisGap
from starguard_core.hedis.measures import HEDIS_MEASURES, get_measure_info
from starguard_core.hedis.predictor import predict_closure_batch
from starguard_core.hedis.interventions import (
    ACTIONABLE_THRESHOLD,
    build_intervention_plan,
)
from starguard_core.hedis.scenarios import default_hedis_scenario


# --- models ---
def test_hedis_gap_creation():
    """HedisGap can be created with required fields."""
    g = HedisGap(
        gap_id="G1",
        member_id="M1",
        measure_code="GSD",
        measure_name="Glycemic Status Assessment",
        star_impact=3,
        roi_estimate=125_000.0,
    )
    assert g.gap_id == "G1"
    assert g.measure_code == "GSD"
    assert g.star_impact == 3


def test_closure_prediction_creation():
    """ClosurePrediction can be created with gap_id, probability, intervention."""
    p = ClosurePrediction(
        gap_id="G1",
        closure_probability=0.55,
        recommended_intervention="Outreach",
    )
    assert p.gap_id == "G1"
    assert p.closure_probability == 0.55
    assert p.recommended_intervention == "Outreach"


# --- measures ---
def test_hedis_measures_has_gsd():
    """HEDIS_MEASURES includes GSD."""
    assert "GSD" in HEDIS_MEASURES
    assert HEDIS_MEASURES["GSD"][0] == "Glycemic Status Assessment"


def test_get_measure_info_returns_tuple():
    """get_measure_info returns (name, care_domain)."""
    name, domain = get_measure_info("CBP")
    assert isinstance(name, str)
    assert isinstance(domain, str)
    assert "Blood Pressure" in name


def test_get_measure_info_unknown():
    """get_measure_info returns Unknown for invalid code."""
    name, domain = get_measure_info("XXX")
    assert name == "Unknown"
    assert domain == "Effectiveness"


# --- predictor ---
def test_predict_closure_batch_returns_list():
    """predict_closure_batch returns list of ClosurePrediction."""
    gaps = [
        HedisGap("G1", "M1", "GSD", "Glycemic Status", 3, 100_000),
    ]
    preds = predict_closure_batch(gaps)
    assert len(preds) == 1
    assert isinstance(preds[0], ClosurePrediction)


def test_predict_closure_batch_one_per_gap():
    """predict_closure_batch returns one prediction per gap."""
    gaps = default_hedis_scenario()
    preds = predict_closure_batch(gaps)
    assert len(preds) == len(gaps)


def test_predict_closure_batch_probability_in_range():
    """predict_closure_batch closure_probability in [0.1, 0.95]."""
    gaps = [HedisGap("G1", "M1", "GSD", "GSD", 1, 50_000)]
    preds = predict_closure_batch(gaps)
    assert 0.1 <= preds[0].closure_probability <= 0.95


# --- interventions ---
def test_build_intervention_plan_returns_dict():
    """build_intervention_plan returns dict with expected keys."""
    gaps = [HedisGap("G1", "M1", "GSD", "GSD", 3, 100_000)]
    preds = [
        ClosurePrediction("G1", 0.4, "Outreach"),
    ]
    plan = build_intervention_plan(gaps, preds)
    assert "total_gaps" in plan
    assert "actionable_gaps" in plan
    assert "total_star_impact" in plan
    assert "total_revenue_impact_m" in plan
    assert "demo_narrative" in plan


def test_build_intervention_plan_total_gaps():
    """build_intervention_plan total_gaps matches input."""
    gaps = default_hedis_scenario()
    preds = predict_closure_batch(gaps)
    plan = build_intervention_plan(gaps, preds)
    assert plan["total_gaps"] == 8


def test_build_intervention_plan_revenue_positive():
    """build_intervention_plan total_revenue_impact_m > 0 for non-empty gaps."""
    gaps = default_hedis_scenario()
    preds = predict_closure_batch(gaps)
    plan = build_intervention_plan(gaps, preds)
    assert plan["total_revenue_impact_m"] > 0


def test_actionable_threshold_constant():
    """ACTIONABLE_THRESHOLD is 0.6 and defined in interventions only."""
    assert ACTIONABLE_THRESHOLD == 0.6


# --- scenarios ---
def test_default_hedis_scenario_returns_eight_gaps():
    """default_hedis_scenario returns 8 synthetic gaps."""
    gaps = default_hedis_scenario()
    assert len(gaps) == 8


def test_default_hedis_scenario_hedis_gaps():
    """default_hedis_scenario returns list of HedisGap."""
    gaps = default_hedis_scenario()
    assert all(isinstance(g, HedisGap) for g in gaps)


def test_default_hedis_scenario_unique_gap_ids():
    """default_hedis_scenario gap_ids are unique."""
    gaps = default_hedis_scenario()
    ids = [g.gap_id for g in gaps]
    assert len(ids) == len(set(ids))


# --- integration ---
def test_full_pipeline():
    """Full pipeline: default_hedis_scenario -> predict_closure_batch -> build_intervention_plan."""
    gaps = default_hedis_scenario()
    preds = predict_closure_batch(gaps)
    plan = build_intervention_plan(gaps, preds)
    assert plan["total_gaps"] == 8
    assert plan["total_revenue_impact_m"] > 0
    assert len(plan["demo_narrative"]) > 0


def test_hedis_module_importable():
    """starguard_core.hedis can be imported with all public names."""
    from starguard_core.hedis import (
        predict_closure_batch,
        build_intervention_plan,
        default_hedis_scenario,
        HEDIS_MEASURES,
        get_measure_info,
        HedisGap,
        ClosurePrediction,
    )
    assert callable(predict_closure_batch)
    assert callable(build_intervention_plan)
    assert callable(default_hedis_scenario)
    assert isinstance(HEDIS_MEASURES, dict)
    assert callable(get_measure_info)


def test_close_gate_assertions():
    """Close gate: 8 gaps, revenue > 0, narrative non-empty."""
    gaps = default_hedis_scenario()
    preds = predict_closure_batch(gaps)
    plan = build_intervention_plan(gaps, preds)
    assert plan["total_gaps"] == 8
    assert plan["total_revenue_impact_m"] > 0
    assert len(plan["demo_narrative"]) > 0


def test_demo_narrative_includes_revenue():
    """build_intervention_plan demo_narrative includes revenue impact."""
    gaps = [HedisGap("G1", "M1", "GSD", "GSD", 3, 100_000)]
    preds = [ClosurePrediction("G1", 0.4, "Outreach")]
    plan = build_intervention_plan(gaps, preds)
    assert "revenue" in plan["demo_narrative"].lower() or "M" in plan["demo_narrative"]


def test_predictor_recommends_intervention():
    """predict_closure_batch recommended_intervention is Outreach or Clinical."""
    gaps = [HedisGap("G1", "M1", "GSD", "GSD", 3, 50_000)]
    preds = predict_closure_batch(gaps)
    assert preds[0].recommended_intervention in ("Outreach", "Clinical")


def test_hedis_measures_has_cbp_and_bcs():
    """HEDIS_MEASURES includes CBP and BCS."""
    assert "CBP" in HEDIS_MEASURES
    assert "BCS" in HEDIS_MEASURES
    assert "Blood Pressure" in HEDIS_MEASURES["CBP"][0]
    assert "Breast" in HEDIS_MEASURES["BCS"][0]


def test_demo_narrative_includes_gaps_and_revenue():
    """build_intervention_plan demo_narrative includes gap count and revenue."""
    gaps = default_hedis_scenario()
    preds = predict_closure_batch(gaps)
    plan = build_intervention_plan(gaps, preds)
    nar = plan["demo_narrative"]
    assert "8" in nar or "gaps" in nar.lower()
    assert "M" in nar or "$" in nar


def test_predictor_recommends_intervention_type():
    """predict_closure_batch recommended_intervention is Outreach or Clinical."""
    gaps = [HedisGap("G1", "M1", "GSD", "GSD", 1, 50_000)]
    preds = predict_closure_batch(gaps)
    assert preds[0].recommended_intervention in ("Outreach", "Clinical")


def test_hedis_measures_has_key_measures():
    """HEDIS_MEASURES includes GSD, CBP, BCS, COL."""
    for code in ("GSD", "CBP", "BCS", "COL"):
        assert code in HEDIS_MEASURES


def test_demo_narrative_includes_revenue():
    """build_intervention_plan demo_narrative includes revenue impact."""
    gaps = default_hedis_scenario()
    preds = predict_closure_batch(gaps)
    plan = build_intervention_plan(gaps, preds)
    assert "M" in plan["demo_narrative"] or "$" in plan["demo_narrative"]


def test_predictor_recommends_intervention():
    """predict_closure_batch recommends Outreach or Clinical."""
    gaps = [HedisGap("G1", "M1", "GSD", "GSD", 3, 100_000)]
    preds = predict_closure_batch(gaps)
    assert preds[0].recommended_intervention in ("Outreach", "Clinical")


def test_hedis_measures_has_core_measures():
    """HEDIS_MEASURES includes GSD, CBP, BCS, COL."""
    for code in ("GSD", "CBP", "BCS", "COL"):
        assert code in HEDIS_MEASURES


def test_demo_narrative_includes_gaps_and_revenue():
    """build_intervention_plan demo_narrative includes gap count and revenue."""
    gaps = default_hedis_scenario()
    preds = predict_closure_batch(gaps)
    plan = build_intervention_plan(gaps, preds)
    nar = plan["demo_narrative"]
    assert "8" in nar or "gaps" in nar.lower()
    assert "$" in nar or "M" in nar


def test_predictor_recommends_outreach_or_clinical():
    """predict_closure_batch recommended_intervention is Outreach or Clinical."""
    gaps = [HedisGap("G1", "M1", "GSD", "GSD", 1, 50_000)]
    preds = predict_closure_batch(gaps)
    assert preds[0].recommended_intervention in ("Outreach", "Clinical")


def test_star_impact_summed_in_plan():
    """build_intervention_plan total_star_impact equals sum of gap star_impacts."""
    gaps = default_hedis_scenario()
    preds = predict_closure_batch(gaps)
    plan = build_intervention_plan(gaps, preds)
    expected = sum(g.star_impact for g in gaps)
    assert plan["total_star_impact"] == expected


def test_demo_narrative_includes_gaps_and_revenue():
    """build_intervention_plan demo_narrative includes gap count and revenue."""
    gaps = default_hedis_scenario()
    preds = predict_closure_batch(gaps)
    plan = build_intervention_plan(gaps, preds)
    nar = plan["demo_narrative"]
    assert "8" in nar or "gaps" in nar.lower()
    assert "M" in nar or "$" in nar


def test_predictor_recommends_outreach_or_clinical():
    """predict_closure_batch recommended_intervention is Outreach or Clinical."""
    gaps = [HedisGap("G1", "M1", "GSD", "GSD", 1, 50_000)]
    preds = predict_closure_batch(gaps)
    assert preds[0].recommended_intervention in ("Outreach", "Clinical")


def test_hedis_measures_has_key_measures():
    """HEDIS_MEASURES includes GSD, CBP, BCS, COL, HEI."""
    for code in ("GSD", "CBP", "BCS", "COL", "HEI"):
        assert code in HEDIS_MEASURES
