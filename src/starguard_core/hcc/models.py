"""HCC risk adjustment — data structures only, no logic."""
from dataclasses import dataclass
from enum import Enum
from typing import Any


class DocumentationStatus(str, Enum):
    """Documentation completeness status."""

    FULL = "full"
    PARTIAL = "partial"
    MISSING = "missing"
    CRITICAL = "critical"


class GapSeverity(str, Enum):
    """Gap severity for revenue impact ordering."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class HCCProfile:
    """Member HCC profile for RAF calculation."""

    member_id: str
    age: int
    gender: str  # M | F
    hcc_codes: list[str]
    documentation_status: DocumentationStatus = DocumentationStatus.FULL


@dataclass
class RAFResult:
    """RAF score result for a profile."""

    profile_id: str
    raf_score: float


@dataclass
class GapResult:
    """Documentation gap with revenue impact."""

    profile_id: str
    hcc_code: str
    severity: GapSeverity
    revenue_impact_usd: float
    documentation_status: DocumentationStatus
