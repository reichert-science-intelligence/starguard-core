"""Star Rating revenue impact — QBP thresholds and revenue per star defined here only."""
from starguard_core.stars.models import PlanProfile
from starguard_core.stars.trajectory import project_stars

# Revenue per star point (annual, per member) — defined here only
REVENUE_PER_STAR_POINT: float = 120.0  # $120/member/year per 1.0 star

# QBP thresholds — defined here only
QBP_THRESHOLD_4_0: float = 4.0  # Crossing 4.0 triggers Quality Bonus Payment
QBP_BONUS_AT_4_0_PCT: float = 0.035  # 3.5% bonus at 4.0 stars
QBP_BONUS_AT_3_5_PCT: float = 0.025  # 2.5% bonus at 3.5 stars
MEDICARE_REVENUE_PER_MEMBER: float = 12_000.0  # ~$12K/year for QBP calc


def _bonus_pct_at_stars(stars: float) -> float:
    """Bonus percentage by star tier (3.0=0%, 3.5=2.5%, 4.0+=3.5%)."""
    if stars < 3.0:
        return 0.0
    if stars < 4.0:
        return QBP_BONUS_AT_3_5_PCT
    return QBP_BONUS_AT_4_0_PCT


def compute_bonus_threshold_impact(
    profile: PlanProfile,
    projected_stars: float | None = None,
    member_count: int | None = None,
) -> dict[str, float | str]:
    """
    Compute QBP threshold impact. A 3.5-star plan crossing 4.0 triggers QBP.
    At 50K members that's $6M+ annually.
    """
    members = member_count or profile.member_count
    proj = projected_stars if projected_stars is not None else project_stars(profile)
    baseline = profile.baseline_stars

    # Medicare revenue per member (~$12K) — QBP is % of this
    REVENUE_PER_MEMBER: float = 12_000.0
    # Bonus % by star tier: 3.0=0%, 3.5=2.5%, 4.0=3.5%, 4.5=4.5%, 5.0=5%
    def _bonus_pct(s: float) -> float:
        if s < 3.0:
            return 0.0
        if s < 3.5:
            return 0.01
        if s < 4.0:
            return 0.025
        if s < 4.5:
            return 0.035
        if s < 5.0:
            return 0.045
        return 0.05

    base_bonus_pct = _bonus_pct(baseline)
    base_revenue = members * base_bonus_pct * REVENUE_PER_MEMBER
    qbp_revenue_4_0 = members * QBP_BONUS_AT_4_0_PCT * REVENUE_PER_MEMBER

    crosses = baseline < QBP_THRESHOLD_4_0 <= proj
    incremental = qbp_revenue_4_0 - base_revenue if crosses else 0.0
    incremental_m = incremental / 1_000_000.0

    narrative = (
        f"Baseline {baseline} stars, projected {proj} stars. "
        f"{'Crosses 4.0 QBP threshold → $' + f'{incremental_m:.1f}' + 'M+ annually' if crosses else 'Below QBP threshold'}"
    )
    return {
        "baseline_stars": baseline,
        "projected_stars": proj,
        "crosses_qbp_threshold": crosses,
        "qbp_revenue_at_4_0_m": round(qbp_revenue_4_0 / 1_000_000.0, 2),
        "incremental_revenue_m": round(incremental_m, 2),
        "demo_narrative": narrative,
    }
