"""Command center tests — four-module compound narrative."""
from starguard_core.command_center import run_command_center


def test_run_command_center_returns_dict():
    """run_command_center returns dict with all module narratives."""
    out = run_command_center()
    assert isinstance(out, dict)
    assert "demo_narrative" in out
    assert "radv_narrative" in out
    assert "hcc_narrative" in out
    assert "hedis_narrative" in out
    assert "stars_narrative" in out


def test_run_command_center_combined_narrative():
    """run_command_center demo_narrative includes all four modules."""
    out = run_command_center()
    nar = out["demo_narrative"]
    assert "RADV" in nar or "radv" in nar.lower()
    assert "HCC" in nar or "hcc" in nar.lower()
    assert "HEDIS" in nar or "hedis" in nar.lower()
    assert "Stars" in nar or "stars" in nar.lower()


def test_run_command_center_hedis_gaps():
    """run_command_center includes hedis_gaps count."""
    out = run_command_center()
    assert out["hedis_gaps"] == 8
