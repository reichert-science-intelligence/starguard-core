"""Star Rating — data structures only, no logic."""
from dataclasses import dataclass
from enum import Enum


class PlanRiskProfile(str, Enum):
    """Plan risk profile for prospect conversation spectrum."""

    LOW = "low"  # 4.5 stars, defend
    MODERATE = "moderate"  # 3.5 stars, improve
    HIGH = "high"  # 2.5 stars, remediate


@dataclass
class PlanProfile:
    """MA plan profile for Star Rating analysis."""

    plan_id: str
    baseline_stars: float
    member_count: int
    risk_profile: PlanRiskProfile
