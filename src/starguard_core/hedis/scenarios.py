"""HEDIS scenarios — 8 synthetic gaps. Imports models only."""
from starguard_core.hedis.models import HedisGap


def default_hedis_scenario() -> list[HedisGap]:
    """Return 8 synthetic HEDIS gaps for close-gate verification."""
    return [
        HedisGap("G1", "M1", "GSD", "Glycemic Status Assessment", 3, 125_000),
        HedisGap("G2", "M1", "CBP", "Controlling Blood Pressure", 3, 98_000),
        HedisGap("G3", "M2", "BCS", "Breast Cancer Screening", 1, 45_000),
        HedisGap("G4", "M2", "COL", "Colorectal Cancer Screening", 1, 52_000),
        HedisGap("G5", "M3", "GSD", "Glycemic Status Assessment", 3, 110_000),
        HedisGap("G6", "M3", "CDC", "Diabetes Care", 2, 78_000),
        HedisGap("G7", "M4", "AWC", "Annual Wellness Check", 2, 65_000),
        HedisGap("G8", "M4", "FUH", "Follow-Up After Hospitalization", 2, 88_000),
    ]
