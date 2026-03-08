"""RAF calculator — CMS demographic weights defined here only. Imports models only."""
from starguard_core.hcc.models import HCCProfile, RAFResult

# CMS demographic weights (age/sex cells) — defined here and nowhere else
_CMS_AGE_SEX_WEIGHTS: dict[tuple[str, str], float] = {
    ("0-34", "M"): 0.341,
    ("0-34", "F"): 0.316,
    ("35-44", "M"): 0.422,
    ("35-44", "F"): 0.398,
    ("45-54", "M"): 0.609,
    ("45-54", "F"): 0.534,
    ("55-59", "M"): 0.827,
    ("55-59", "F"): 0.691,
    ("60-64", "M"): 1.038,
    ("60-64", "F"): 0.871,
    ("65-69", "M"): 1.095,
    ("65-69", "F"): 0.955,
    ("70-74", "M"): 1.165,
    ("70-74", "F"): 1.012,
    ("75-79", "M"): 1.248,
    ("75-79", "F"): 1.092,
    ("80+", "M"): 1.365,
    ("80+", "F"): 1.198,
}

# HCC weight stub (simplified; full CMS model has 100+ HCCs)
_HCC_WEIGHTS: dict[str, float] = {
    "HCC001": 0.331,
    "HCC002": 0.501,
    "HCC008": 0.344,
    "HCC018": 0.289,
    "HCC036": 0.394,
    "HCC055": 0.326,
    "HCC108": 0.382,
    "HCC111": 0.441,
    "HCC154": 0.367,
    "HCC226": 0.512,
}


def _age_bucket(age: int) -> str:
    """Map age to CMS age bucket."""
    if age < 35:
        return "0-34"
    if age < 45:
        return "35-44"
    if age < 55:
        return "45-54"
    if age < 60:
        return "55-59"
    if age < 65:
        return "60-64"
    if age < 70:
        return "65-69"
    if age < 75:
        return "70-74"
    if age < 80:
        return "75-79"
    return "80+"


def compute_raf_score(profile: HCCProfile) -> RAFResult:
    """Compute RAF score for a single profile."""
    bucket = _age_bucket(profile.age)
    key = (bucket, "M" if profile.gender.upper().startswith("M") else "F")
    base = _CMS_AGE_SEX_WEIGHTS.get(key, 0.5)
    hcc_sum = sum(_HCC_WEIGHTS.get(c, 0.2) for c in profile.hcc_codes)
    raf = base + hcc_sum
    return RAFResult(profile_id=profile.member_id, raf_score=round(raf, 4))


def compute_raf_batch(profiles: list[HCCProfile]) -> list[RAFResult]:
    """Compute RAF scores for multiple profiles."""
    return [compute_raf_score(p) for p in profiles]
