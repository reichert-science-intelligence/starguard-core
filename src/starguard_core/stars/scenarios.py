"""Star Rating scenarios — 3 plan risk profiles. Imports models only."""
from starguard_core.stars.models import PlanProfile, PlanRiskProfile


def default_stars_scenario() -> list[PlanProfile]:
    """Return 3 synthetic plan profiles: Low (4.5), Moderate (3.5), High (2.5)."""
    return [
        PlanProfile(
            plan_id="P1",
            baseline_stars=4.5,
            member_count=50_000,
            risk_profile=PlanRiskProfile.LOW,
        ),
        PlanProfile(
            plan_id="P2",
            baseline_stars=3.5,
            member_count=50_000,
            risk_profile=PlanRiskProfile.MODERATE,
        ),
        PlanProfile(
            plan_id="P3",
            baseline_stars=2.5,
            member_count=100_000,
            risk_profile=PlanRiskProfile.HIGH,
        ),
    ]
