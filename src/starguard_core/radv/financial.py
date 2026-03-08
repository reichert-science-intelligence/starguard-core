"""RADV financial calculations — imports models only."""
from starguard_core.radv.models import RadvScenario


def compute_exposure(scenario: RadvScenario) -> float:
    """Compute estimated financial exposure. Stub."""
    return scenario.enrollee_count * scenario.error_rate * 1000.0
