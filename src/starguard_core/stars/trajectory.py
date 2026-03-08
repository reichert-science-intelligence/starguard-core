"""Star Rating trajectory — improvement rate defined here only. Imports models only."""
from starguard_core.stars.models import PlanProfile

# Improvement rate constant — defined here and nowhere else
# 0.5 = 3.5 -> 4.0 in 12 months (Moderate crosses QBP threshold)
IMPROVEMENT_RATE: float = 0.5


def project_stars(profile: PlanProfile, months: int = 12) -> float:
    """Project star rating after intervention period. Conservative model."""
    delta = IMPROVEMENT_RATE * (months / 12.0)
    projected = min(5.0, profile.baseline_stars + delta)
    return round(projected, 2)


def crosses_qbp_threshold(baseline: float, projected: float, threshold: float = 4.0) -> bool:
    """True if trajectory crosses QBP threshold (e.g. 3.5 -> 4.0)."""
    return baseline < threshold <= projected
