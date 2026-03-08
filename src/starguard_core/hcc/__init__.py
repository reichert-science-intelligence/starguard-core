"""HCC risk adjustment — public API surface."""
from starguard_core.hcc import calculator
from starguard_core.hcc import gaps
from starguard_core.hcc import models
from starguard_core.hcc import revenue
from starguard_core.hcc import scenarios
from starguard_core.hcc.calculator import compute_raf_batch, compute_raf_score
from starguard_core.hcc.gaps import identify_chronic_gaps
from starguard_core.hcc.revenue import compute_revenue_opportunity
from starguard_core.hcc.scenarios import default_hcc_scenario

__all__ = [
    "models",
    "calculator",
    "gaps",
    "revenue",
    "scenarios",
    "compute_raf_score",
    "compute_raf_batch",
    "identify_chronic_gaps",
    "compute_revenue_opportunity",
    "default_hcc_scenario",
    "run_compound_analysis",
]


def run_compound_analysis(
    radv_exposure_score: float,
    raf_documentation_gap_rate: float,
) -> dict[str, float | str]:
    """
    Wire RADV exposure score × RAF documentation gap rate into compound score.
    Anchor for $2.3M prospect story in AuditShield.
    """
    compound_score = radv_exposure_score * raf_documentation_gap_rate
    demo_narrative = (
        f"Compound score {compound_score:.2f} "
        f"(RADV {radv_exposure_score:.2f} × gap rate {raf_documentation_gap_rate:.2%}) "
        "→ $2.3M prospect opportunity"
    )
    return {
        "compound_score": round(compound_score, 4),
        "radv_exposure_score": radv_exposure_score,
        "raf_gap_rate": raf_documentation_gap_rate,
        "demo_narrative": demo_narrative,
    }
