"""HCC scenarios — 5 synthetic profiles. Imports models only."""
from starguard_core.hcc.models import DocumentationStatus, HCCProfile


def default_hcc_scenario() -> list[HCCProfile]:
    """Return 5 synthetic profiles across full/partial/missing/critical documentation states."""
    return [
        HCCProfile(
            member_id="S1",
            age=68,
            gender="M",
            hcc_codes=["HCC036", "HCC226"],
            documentation_status=DocumentationStatus.FULL,
        ),
        HCCProfile(
            member_id="S2",
            age=72,
            gender="F",
            hcc_codes=["HCC111", "HCC154"],
            documentation_status=DocumentationStatus.PARTIAL,
        ),
        HCCProfile(
            member_id="S3",
            age=58,
            gender="M",
            hcc_codes=["HCC008", "HCC055"],
            documentation_status=DocumentationStatus.MISSING,
        ),
        HCCProfile(
            member_id="S4",
            age=78,
            gender="F",
            hcc_codes=["HCC001", "HCC002", "HCC108"],
            documentation_status=DocumentationStatus.CRITICAL,
        ),
        HCCProfile(
            member_id="S5",
            age=45,
            gender="M",
            hcc_codes=[],
            documentation_status=DocumentationStatus.FULL,
        ),
    ]
