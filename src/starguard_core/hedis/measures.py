"""HEDIS measure definitions — NCQA MY2025 alignment."""

# Measure code -> (name, care_domain)
HEDIS_MEASURES: dict[str, tuple[str, str]] = {
    "CBP": ("Controlling Blood Pressure", "Effectiveness"),
    "CDC": ("Diabetes Care", "Effectiveness"),
    "W34": ("Well-Child Visits", "Effectiveness"),
    "AWC": ("Annual Wellness Check", "Effectiveness"),
    "FUH": ("Follow-Up After Hospitalization", "Effectiveness"),
    "PCE": ("Pharmacotherapy for COPD", "Effectiveness"),
    "MPM": ("Medication Management", "Effectiveness"),
    "COA": ("Care of Older Adults", "Effectiveness"),
    "GSD": ("Glycemic Status Assessment", "Effectiveness"),
    "BCS": ("Breast Cancer Screening", "Effectiveness"),
    "COL": ("Colorectal Cancer Screening", "Effectiveness"),
    "HEI": ("Health Equity Index", "Experience"),
}


def get_measure_info(measure_code: str) -> tuple[str, str]:
    """Return (measure_name, care_domain) for a measure code."""
    return HEDIS_MEASURES.get(measure_code, ("Unknown", "Effectiveness"))
