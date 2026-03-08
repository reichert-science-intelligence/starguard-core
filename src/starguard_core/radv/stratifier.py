"""RADV stratifier — imports models only."""
from typing import Any

from starguard_core.radv.models import RadvScenario


def stratify(scenario: RadvScenario) -> dict[str, Any]:
    """Stratify scenario by risk segments. Returns risk_tier: low | medium | high."""
    if scenario.error_rate < 0.03:
        tier = "low"
    elif scenario.error_rate < 0.08:
        tier = "medium"
    else:
        tier = "high"
    return {"segments": 1, "scenario": scenario, "risk_tier": tier}
