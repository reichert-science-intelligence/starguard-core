"""RADV exposure scorer — orchestrates stratifier and financial."""
from starguard_core.radv.models import RadvResult, RadvScenario
from starguard_core.radv.stratifier import stratify
from starguard_core.radv.financial import compute_exposure


def score_exposure(scenario: RadvScenario) -> RadvResult:
    """Compute RADV audit exposure from scenario parameters."""
    stratify(scenario)  # stratify for risk segments
    exposure = compute_exposure(scenario)
    return RadvResult(
        estimated_exposure=exposure,
        confidence_interval=(exposure * 0.9, exposure * 1.1),
        scenario=scenario,
    )
