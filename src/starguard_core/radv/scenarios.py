"""RADV scenarios — imports models only."""
from starguard_core.radv.models import RadvScenario


def default_scenario() -> RadvScenario:
    """Return default RADV scenario. Stub."""
    return RadvScenario(
        enrollee_count=1000,
        sample_size=200,
        error_rate=0.05,
    )
