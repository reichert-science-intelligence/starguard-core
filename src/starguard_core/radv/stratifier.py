"""RADV stratifier — imports models only."""
from typing import Any

from starguard_core.radv.models import RadvScenario


def stratify(scenario: RadvScenario) -> dict[str, Any]:
    """Stratify scenario by risk segments. Stub."""
    return {"segments": 1, "scenario": scenario}
