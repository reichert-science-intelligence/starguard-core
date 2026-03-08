"""HCC module tests — 20 stubs, all should pass."""
import pytest

from starguard_core.hcc.models import (
    DocumentationStatus,
    GapResult,
    GapSeverity,
    HCCProfile,
    RAFResult,
)
from starguard_core.hcc.calculator import compute_raf_batch, compute_raf_score
from starguard_core.hcc.gaps import identify_chronic_gaps
from starguard_core.hcc.revenue import RECAPTURE_RATE, compute_revenue_opportunity
from starguard_core.hcc.scenarios import default_hcc_scenario
from starguard_core.hcc import run_compound_analysis


# --- models ---
def test_hcc_profile_creation():
    """HCCProfile can be created with required fields."""
    p = HCCProfile(member_id="M1", age=65, gender="M", hcc_codes=["HCC036"])
    assert p.member_id == "M1"
    assert p.age == 65
    assert p.hcc_codes == ["HCC036"]


def test_hcc_profile_default_documentation():
    """HCCProfile documentation_status defaults to FULL."""
    p = HCCProfile(member_id="M1", age=50, gender="F", hcc_codes=[])
    assert p.documentation_status == DocumentationStatus.FULL


def test_raf_result_creation():
    """RAFResult can be created with profile_id and raf_score."""
    r = RAFResult(profile_id="M1", raf_score=1.25)
    assert r.profile_id == "M1"
    assert r.raf_score == 1.25


def test_gap_result_creation():
    """GapResult can be created with all required fields."""
    g = GapResult(
        profile_id="M1",
        hcc_code="HCC226",
        severity=GapSeverity.HIGH,
        revenue_impact_usd=3500.0,
        documentation_status=DocumentationStatus.MISSING,
    )
    assert g.profile_id == "M1"
    assert g.revenue_impact_usd == 3500.0


# --- calculator ---
def test_compute_raf_score_returns_raf_result():
    """compute_raf_score returns RAFResult."""
    p = HCCProfile(member_id="M1", age=68, gender="M", hcc_codes=["HCC036"])
    r = compute_raf_score(p)
    assert isinstance(r, RAFResult)
    assert r.profile_id == "M1"


def test_compute_raf_score_positive():
    """compute_raf_score returns positive RAF for valid profile."""
    p = HCCProfile(member_id="M1", age=70, gender="F", hcc_codes=["HCC111"])
    r = compute_raf_score(p)
    assert r.raf_score > 0


def test_compute_raf_batch_returns_list():
    """compute_raf_batch returns list of RAFResult."""
    profiles = [
        HCCProfile(member_id="M1", age=60, gender="M", hcc_codes=[]),
        HCCProfile(member_id="M2", age=75, gender="F", hcc_codes=["HCC226"]),
    ]
    results = compute_raf_batch(profiles)
    assert len(results) == 2
    assert all(isinstance(r, RAFResult) for r in results)


# --- gaps ---
def test_identify_chronic_gaps_full_returns_empty():
    """identify_chronic_gaps returns empty for FULL documentation."""
    p = HCCProfile(
        member_id="M1",
        age=65,
        gender="M",
        hcc_codes=["HCC036"],
        documentation_status=DocumentationStatus.FULL,
    )
    gaps = identify_chronic_gaps(p)
    assert gaps == []


def test_identify_chronic_gaps_returns_sorted_by_revenue():
    """identify_chronic_gaps returns sorted by revenue impact descending."""
    p = HCCProfile(
        member_id="M1",
        age=65,
        gender="M",
        hcc_codes=["HCC036", "HCC226"],
        documentation_status=DocumentationStatus.MISSING,
    )
    gaps = identify_chronic_gaps(p)
    assert len(gaps) >= 1
    revs = [g.revenue_impact_usd for g in gaps]
    assert revs == sorted(revs, reverse=True)


def test_identify_chronic_gaps_returns_gap_results():
    """identify_chronic_gaps returns list of GapResult."""
    p = HCCProfile(
        member_id="M1",
        age=58,
        gender="F",
        hcc_codes=["HCC008"],
        documentation_status=DocumentationStatus.PARTIAL,
    )
    gaps = identify_chronic_gaps(p)
    assert all(isinstance(g, GapResult) for g in gaps)


# --- revenue ---
def test_compute_revenue_opportunity_returns_dict():
    """compute_revenue_opportunity returns dict with expected keys."""
    raf = [RAFResult(profile_id="M1", raf_score=1.2)]
    gaps = [
        GapResult(
            profile_id="M1",
            hcc_code="HCC036",
            severity=GapSeverity.MEDIUM,
            revenue_impact_usd=1500.0,
            documentation_status=DocumentationStatus.PARTIAL,
        )
    ]
    out = compute_revenue_opportunity(raf, gaps)
    assert isinstance(out, dict)
    assert "average_raf_score" in out
    assert "total_gaps_identified" in out
    assert "net_opportunity_usd" in out
    assert "demo_narrative" in out


def test_compute_revenue_opportunity_demo_narrative_string():
    """compute_revenue_opportunity produces demo_narrative string."""
    raf = [RAFResult(profile_id="M1", raf_score=1.0)]
    gaps = []
    out = compute_revenue_opportunity(raf, gaps)
    assert isinstance(out["demo_narrative"], str)
    assert len(out["demo_narrative"]) > 0


def test_recapture_rate_constant():
    """Recapture rate is 0.85 and defined in revenue module only."""
    assert RECAPTURE_RATE == 0.85


# --- scenarios ---
def test_default_hcc_scenario_returns_five_profiles():
    """default_hcc_scenario returns 5 synthetic profiles."""
    profiles = default_hcc_scenario()
    assert len(profiles) == 5


def test_default_hcc_scenario_covers_documentation_states():
    """default_hcc_scenario covers full/partial/missing/critical states."""
    profiles = default_hcc_scenario()
    statuses = {p.documentation_status for p in profiles}
    assert DocumentationStatus.FULL in statuses
    assert DocumentationStatus.PARTIAL in statuses
    assert DocumentationStatus.MISSING in statuses
    assert DocumentationStatus.CRITICAL in statuses


# --- compound analysis ---
def test_run_compound_analysis_returns_dict():
    """run_compound_analysis returns dict with compound_score and demo_narrative."""
    out = run_compound_analysis(radv_exposure_score=1.5, raf_documentation_gap_rate=0.25)
    assert "compound_score" in out
    assert "demo_narrative" in out
    assert isinstance(out["compound_score"], (int, float))
    assert isinstance(out["demo_narrative"], str)


def test_run_compound_analysis_compound_score():
    """run_compound_analysis compound_score = radv × gap_rate."""
    out = run_compound_analysis(radv_exposure_score=2.0, raf_documentation_gap_rate=0.5)
    assert abs(out["compound_score"] - 1.0) < 0.01


def test_run_compound_analysis_demo_narrative_prospect():
    """run_compound_analysis demo_narrative includes prospect opportunity."""
    out = run_compound_analysis(radv_exposure_score=1.0, raf_documentation_gap_rate=0.3)
    assert "2.3M" in out["demo_narrative"] or "prospect" in out["demo_narrative"].lower()


# --- integration ---
def test_full_pipeline():
    """Full pipeline: default_hcc_scenario -> compute_raf_batch -> identify_chronic_gaps -> compute_revenue_opportunity."""
    profiles = default_hcc_scenario()
    raf_results = compute_raf_batch(profiles)
    gaps = []
    for p in profiles:
        gaps.extend(identify_chronic_gaps(p))
    summary = compute_revenue_opportunity(raf_results, gaps)
    assert summary["average_raf_score"] >= 0
    assert summary["total_gaps_identified"] >= 0
    assert "demo_narrative" in summary


def test_hcc_module_importable():
    """starguard_core.hcc can be imported with all public names."""
    from starguard_core.hcc import (
        compute_raf_batch,
        compute_raf_score,
        identify_chronic_gaps,
        compute_revenue_opportunity,
        default_hcc_scenario,
        run_compound_analysis,
    )
    assert callable(compute_raf_score)
    assert callable(compute_raf_batch)
    assert callable(identify_chronic_gaps)
    assert callable(compute_revenue_opportunity)
    assert callable(default_hcc_scenario)
    assert callable(run_compound_analysis)
