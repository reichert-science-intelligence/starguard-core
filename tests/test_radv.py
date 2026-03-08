"""RADV module tests — 19 stubs, all should pass."""
import pytest

from starguard_core.radv.models import RadvResult, RadvScenario
from starguard_core.radv.scorer import score_exposure
from starguard_core.radv.stratifier import stratify
from starguard_core.radv.financial import compute_exposure
from starguard_core.radv.scenarios import default_scenario


# --- models ---
def test_radv_scenario_creation():
    """RadvScenario can be created with required fields."""
    s = RadvScenario(enrollee_count=1000, sample_size=200, error_rate=0.05)
    assert s.enrollee_count == 1000
    assert s.sample_size == 200
    assert s.error_rate == 0.05


def test_radv_scenario_default_extrapolation():
    """RadvScenario extrapolation_factor defaults to 1.0."""
    s = RadvScenario(enrollee_count=500, sample_size=100, error_rate=0.08)
    assert s.extrapolation_factor == 1.0


def test_radv_result_creation():
    """RadvResult can be created with required fields."""
    s = RadvScenario(enrollee_count=1000, sample_size=200, error_rate=0.05)
    r = RadvResult(estimated_exposure=50_000.0, confidence_interval=(45_000, 55_000), scenario=s)
    assert r.estimated_exposure == 50_000.0
    assert r.confidence_interval == (45_000, 55_000)


# --- stratifier ---
def test_stratify_returns_dict():
    """stratify returns a dict with segments."""
    s = RadvScenario(enrollee_count=1000, sample_size=200, error_rate=0.05)
    out = stratify(s)
    assert isinstance(out, dict)
    assert "segments" in out


def test_stratify_includes_scenario():
    """stratify output includes scenario reference."""
    s = RadvScenario(enrollee_count=500, sample_size=100, error_rate=0.08)
    out = stratify(s)
    assert out.get("scenario") is s


# --- financial ---
def test_compute_exposure_returns_float():
    """compute_exposure returns a float."""
    s = RadvScenario(enrollee_count=1000, sample_size=200, error_rate=0.05)
    out = compute_exposure(s)
    assert isinstance(out, float)


def test_compute_exposure_positive():
    """compute_exposure returns positive value for valid scenario."""
    s = RadvScenario(enrollee_count=1000, sample_size=200, error_rate=0.05)
    out = compute_exposure(s)
    assert out > 0


def test_compute_exposure_zero_error():
    """compute_exposure returns 0 for zero error rate."""
    s = RadvScenario(enrollee_count=1000, sample_size=200, error_rate=0.0)
    out = compute_exposure(s)
    assert out == 0.0


# --- scenarios ---
def test_default_scenario_returns_radv_scenario():
    """default_scenario returns RadvScenario."""
    s = default_scenario()
    assert isinstance(s, RadvScenario)


def test_default_scenario_has_reasonable_values():
    """default_scenario has reasonable enrollee/sample/error values."""
    s = default_scenario()
    assert s.enrollee_count > 0
    assert s.sample_size > 0
    assert 0 <= s.error_rate <= 1


# --- scorer ---
def test_score_exposure_returns_radv_result():
    """score_exposure returns RadvResult."""
    s = RadvScenario(enrollee_count=1000, sample_size=200, error_rate=0.05)
    r = score_exposure(s)
    assert isinstance(r, RadvResult)


def test_score_exposure_has_confidence_interval():
    """score_exposure result has non-empty confidence interval."""
    s = RadvScenario(enrollee_count=1000, sample_size=200, error_rate=0.05)
    r = score_exposure(s)
    assert len(r.confidence_interval) == 2
    assert r.confidence_interval[0] <= r.confidence_interval[1]


def test_score_exposure_links_scenario():
    """score_exposure result links back to input scenario."""
    s = RadvScenario(enrollee_count=500, sample_size=100, error_rate=0.08)
    r = score_exposure(s)
    assert r.scenario is s


# --- integration ---
def test_full_pipeline():
    """Full pipeline: default_scenario -> score_exposure -> valid result."""
    s = default_scenario()
    r = score_exposure(s)
    assert r.estimated_exposure >= 0
    assert r.scenario.enrollee_count == s.enrollee_count


def test_radv_module_importable():
    """starguard_core.radv can be imported."""
    import starguard_core.radv as radv
    assert hasattr(radv, "models")
    assert hasattr(radv, "scorer")
    assert hasattr(radv, "stratifier")
    assert hasattr(radv, "financial")
    assert hasattr(radv, "scenarios")


def test_radv_models_export():
    """models module exports RadvScenario and RadvResult."""
    from starguard_core.radv import models
    assert hasattr(models, "RadvScenario")
    assert hasattr(models, "RadvResult")


def test_radv_scorer_export():
    """scorer module exports score_exposure."""
    from starguard_core.radv import scorer
    assert hasattr(scorer, "score_exposure")


def test_radv_stratifier_export():
    """stratifier module exports stratify."""
    from starguard_core.radv import stratifier
    assert hasattr(stratifier, "stratify")


def test_radv_financial_export():
    """financial module exports compute_exposure."""
    from starguard_core.radv import financial
    assert hasattr(financial, "compute_exposure")
