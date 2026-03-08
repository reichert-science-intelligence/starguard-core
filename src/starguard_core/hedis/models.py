"""HEDIS gap closure — data structures only, no logic."""
from dataclasses import dataclass


@dataclass
class HedisGap:
    """HEDIS care gap for a member-measure pair."""

    gap_id: str
    member_id: str
    measure_code: str
    measure_name: str
    star_impact: int  # 1–5 weighting
    roi_estimate: float  # USD


@dataclass
class ClosurePrediction:
    """Prediction for gap closure likelihood."""

    gap_id: str
    closure_probability: float
    recommended_intervention: str
