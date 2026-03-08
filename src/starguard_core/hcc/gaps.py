"""Gap identification — severity thresholds defined here only. Imports models only."""
from starguard_core.hcc.models import (
    DocumentationStatus,
    GapResult,
    GapSeverity,
    HCCProfile,
)

# Severity thresholds — defined here and nowhere else
_SEVERITY_THRESHOLDS: dict[DocumentationStatus, GapSeverity] = {
    DocumentationStatus.FULL: GapSeverity.LOW,
    DocumentationStatus.PARTIAL: GapSeverity.MEDIUM,
    DocumentationStatus.MISSING: GapSeverity.HIGH,
    DocumentationStatus.CRITICAL: GapSeverity.CRITICAL,
}

# Revenue impact by severity (for sorting)
_SEVERITY_REVENUE: dict[GapSeverity, float] = {
    GapSeverity.LOW: 500,
    GapSeverity.MEDIUM: 1500,
    GapSeverity.HIGH: 3500,
    GapSeverity.CRITICAL: 7500,
}


def identify_chronic_gaps(profile: HCCProfile) -> list[GapResult]:
    """Identify documentation gaps for a profile. Returns sorted by revenue impact descending."""
    gaps: list[GapResult] = []
    status = profile.documentation_status
    if status == DocumentationStatus.FULL:
        return []
    severity = _SEVERITY_THRESHOLDS.get(status, GapSeverity.MEDIUM)
    impact = _SEVERITY_REVENUE.get(severity, 1500)
    for hcc in profile.hcc_codes:
        gaps.append(
            GapResult(
                profile_id=profile.member_id,
                hcc_code=hcc,
                severity=severity,
                revenue_impact_usd=impact,
                documentation_status=status,
            )
        )
    gaps.sort(key=lambda g: g.revenue_impact_usd, reverse=True)
    return gaps
