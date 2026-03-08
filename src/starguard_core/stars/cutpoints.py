"""CMS Star Rating cut-points — defined here only."""

# CMS percentile-to-stars cut-points (simplified; full CMS has measure-specific)
# Percentile threshold -> star rating
_CMS_CUTPOINTS: dict[float, float] = {
    95.0: 5.0,
    90.0: 4.0,
    85.0: 3.0,
    75.0: 2.0,
    0.0: 1.0,
}


def percentile_to_stars(percentile: float) -> float:
    """Convert percentile to star rating using CMS cut-points."""
    sorted_cuts = sorted(_CMS_CUTPOINTS.keys(), reverse=True)
    for cut in sorted_cuts:
        if percentile >= cut:
            return _CMS_CUTPOINTS[cut]
    return 1.0


def stars_to_percentile(stars: float) -> float:
    """Convert star rating to approximate percentile (inverse of cut-points)."""
    rev_map = {v: k for k, v in _CMS_CUTPOINTS.items()}
    return rev_map.get(stars, 85.0)
