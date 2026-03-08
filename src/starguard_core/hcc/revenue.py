"""Revenue opportunity — recapture rate defined here only. Imports models only."""
from starguard_core.hcc.models import GapResult, RAFResult

# Recapture rate constant — defined here and nowhere else
RECAPTURE_RATE: float = 0.85


def compute_revenue_opportunity(
    raf_results: list[RAFResult], gaps: list[GapResult]
) -> dict[str, float | str]:
    """Compute net revenue opportunity. Produces demo_narrative string."""
    avg_raf = (
        sum(r.raf_score for r in raf_results) / len(raf_results)
        if raf_results
        else 0.0
    )
    total_gap_revenue = sum(g.revenue_impact_usd for g in gaps)
    net_opportunity = total_gap_revenue * RECAPTURE_RATE
    demo_narrative = (
        f"RAF avg {avg_raf:.2f}, {len(gaps)} gaps → "
        f"${net_opportunity:,.0f} recapture opportunity (rate {RECAPTURE_RATE})"
    )
    return {
        "average_raf_score": round(avg_raf, 4),
        "total_gaps_identified": len(gaps),
        "net_opportunity_usd": round(net_opportunity, 2),
        "demo_narrative": demo_narrative,
    }
