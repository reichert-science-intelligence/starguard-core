"""Star Rating — public API surface."""
from starguard_core.stars import cutpoints
from starguard_core.stars import impact
from starguard_core.stars import models
from starguard_core.stars import scenarios
from starguard_core.stars import trajectory
from starguard_core.stars.cutpoints import percentile_to_stars, stars_to_percentile
from starguard_core.stars.impact import (
    QBP_BONUS_AT_4_0_PCT,
    QBP_THRESHOLD_4_0,
    REVENUE_PER_STAR_POINT,
    compute_bonus_threshold_impact,
)
from starguard_core.stars.models import PlanProfile, PlanRiskProfile
from starguard_core.stars.scenarios import default_stars_scenario
from starguard_core.stars.trajectory import (
    IMPROVEMENT_RATE,
    crosses_qbp_threshold,
    project_stars,
)

__all__ = [
    "models",
    "cutpoints",
    "trajectory",
    "impact",
    "scenarios",
    "PlanProfile",
    "PlanRiskProfile",
    "percentile_to_stars",
    "stars_to_percentile",
    "project_stars",
    "crosses_qbp_threshold",
    "compute_bonus_threshold_impact",
    "default_stars_scenario",
    "IMPROVEMENT_RATE",
    "REVENUE_PER_STAR_POINT",
    "QBP_THRESHOLD_4_0",
    "QBP_BONUS_AT_4_0_PCT",
]
