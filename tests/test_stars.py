"""Stars module tests — 22 stubs, all should pass."""
import pytest

from starguard_core.stars.models import PlanProfile, PlanRiskProfile
from starguard_core.stars.cutpoints import percentile_to_stars, stars_to_percentile
from starguard_core.stars.trajectory import IMPROVEMENT_RATE, project_stars, crosses_qbp_threshold
from starguard_core.stars.impact import (
    REVENUE_PER_STAR_POINT,
    QBP_THRESHOLD_4_0,
    QBP_BONUS_AT_4_0_PCT,
    compute_bonus_threshold_impact,
)
from starguard_core.stars.scenarios import default_stars_scenario
from starguard_core.stars import (
    default_stars_scenario as default_scenario,
    compute_bonus_threshold_impact as compute_impact,
    project_stars as proj_stars,
)


# --- models ---
def test_plan_profile_creation():
    """PlanProfile can be created with required fields."""
    p = PlanProfile(plan_id="P1", baseline_stars=4.5, member_count=50_000, risk_profile=PlanRiskProfile.LOW)
    assert p.plan_id == "P1"
    assert p.baseline_stars == 4.5
    assert p.member_count == 50_000


def test_plan_risk_profile_enum():
    """PlanRiskProfile has LOW, MODERATE, HIGH."""
    assert PlanRiskProfile.LOW.value == "low"
    assert PlanRiskProfile.MODERATE.value == "moderate"
    assert PlanRiskProfile.HIGH.value == "high"


# --- cutpoints ---
def test_percentile_to_stars_95():
    """percentile_to_stars(95) returns 5.0."""
    assert percentile_to_stars(95.0) == 5.0


def test_percentile_to_stars_90():
    """percentile_to_stars(90) returns 4.0."""
    assert percentile_to_stars(90.0) == 4.0


def test_percentile_to_stars_85():
    """percentile_to_stars(85) returns 3.0."""
    assert percentile_to_stars(85.0) == 3.0


def test_stars_to_percentile_inverse():
    """stars_to_percentile returns approximate inverse."""
    assert stars_to_percentile(5.0) == 95.0
    assert stars_to_percentile(4.0) == 90.0


# --- trajectory ---
def test_improvement_rate_constant():
    """IMPROVEMENT_RATE is 0.5 and defined in trajectory only."""
    assert IMPROVEMENT_RATE == 0.5


def test_project_stars_increases():
    """project_stars returns value >= baseline."""
    p = PlanProfile("P1", 3.5, 50_000, PlanRiskProfile.MODERATE)
    proj = project_stars(p)
    assert proj >= 3.5


def test_project_stars_capped_at_5():
    """project_stars caps at 5.0."""
    p = PlanProfile("P1", 4.9, 50_000, PlanRiskProfile.LOW)
    proj = project_stars(p)
    assert proj <= 5.0


def test_crosses_qbp_threshold_true():
    """crosses_qbp_threshold(3.5, 4.0) returns True."""
    assert crosses_qbp_threshold(3.5, 4.0) is True


def test_crosses_qbp_threshold_false():
    """crosses_qbp_threshold(4.0, 4.5) returns False (already above)."""
    assert crosses_qbp_threshold(4.0, 4.5) is False


# --- impact ---
def test_revenue_per_star_point_constant():
    """REVENUE_PER_STAR_POINT is 120 and defined in impact only."""
    assert REVENUE_PER_STAR_POINT == 120.0


def test_qbp_threshold_constant():
    """QBP_THRESHOLD_4_0 is 4.0."""
    assert QBP_THRESHOLD_4_0 == 4.0


def test_compute_bonus_threshold_impact_returns_dict():
    """compute_bonus_threshold_impact returns dict with expected keys."""
    p = PlanProfile("P1", 3.5, 50_000, PlanRiskProfile.MODERATE)
    out = compute_bonus_threshold_impact(p)
    assert "baseline_stars" in out
    assert "projected_stars" in out
    assert "crosses_qbp_threshold" in out
    assert "qbp_revenue_at_4_0_m" in out
    assert "demo_narrative" in out


def test_compute_bonus_threshold_impact_moderate_crosses():
    """Moderate profile (3.5) crosses 4.0 QBP threshold."""
    profiles = default_stars_scenario()
    moderate = profiles[1]
    out = compute_bonus_threshold_impact(moderate)
    assert out["crosses_qbp_threshold"] is True


def test_qbp_revenue_at_50k_positive():
    """QBP revenue at 4.0 for 50K members is positive."""
    p = PlanProfile("P1", 3.5, 50_000, PlanRiskProfile.MODERATE)
    out = compute_bonus_threshold_impact(p)
    assert out["qbp_revenue_at_4_0_m"] > 0


# --- scenarios ---
def test_default_stars_scenario_returns_three():
    """default_stars_scenario returns 3 profiles."""
    profiles = default_stars_scenario()
    assert len(profiles) == 3


def test_default_stars_scenario_covers_risk_profiles():
    """default_stars_scenario covers Low, Moderate, High."""
    profiles = default_stars_scenario()
    risk_profiles = {p.risk_profile for p in profiles}
    assert PlanRiskProfile.LOW in risk_profiles
    assert PlanRiskProfile.MODERATE in risk_profiles
    assert PlanRiskProfile.HIGH in risk_profiles


def test_default_stars_scenario_baseline_values():
    """default_stars_scenario has 4.5, 3.5, 2.5 baseline stars."""
    profiles = default_stars_scenario()
    stars = [p.baseline_stars for p in profiles]
    assert 4.5 in stars
    assert 3.5 in stars
    assert 2.5 in stars


# --- integration ---
def test_full_pipeline():
    """Full pipeline: default_stars_scenario -> compute_bonus_threshold_impact."""
    profiles = default_stars_scenario()
    for p in profiles:
        out = compute_bonus_threshold_impact(p)
        assert out["baseline_stars"] == p.baseline_stars
        assert len(out["demo_narrative"]) > 0


def test_stars_module_importable():
    """starguard_core.stars can be imported with all public names."""
    from starguard_core.stars import (
        default_stars_scenario,
        compute_bonus_threshold_impact,
        project_stars,
        percentile_to_stars,
    )
    assert callable(default_stars_scenario)
    assert callable(compute_bonus_threshold_impact)
    assert callable(project_stars)
    assert callable(percentile_to_stars)
