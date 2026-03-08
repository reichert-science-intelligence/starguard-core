"""RADV audit exposure calculator — data structures only, no logic."""
from dataclasses import dataclass
from typing import Any


@dataclass
class RadvScenario:
    """RADV audit scenario parameters."""

    enrollee_count: int
    sample_size: int
    error_rate: float
    extrapolation_factor: float = 1.0


@dataclass
class RadvResult:
    """RADV audit exposure result."""

    estimated_exposure: float
    confidence_interval: tuple[float, float]
    scenario: RadvScenario
