# verify_hedis_flags.py
"""Verify HEDIS feature flags: FREE gets summary, PRO gets predictions."""
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from starguard_core.auth.validator import get_tier_config, is_feature_enabled

cfg_free = get_tier_config(None)
cfg_pro = get_tier_config("pro-TESTKEY0000000001")

assert is_feature_enabled("hedis_summary", cfg_free), "FAIL: FREE hedis_summary"
assert not is_feature_enabled("hedis_predictions", cfg_free), "FAIL: FREE hedis_predictions"
assert is_feature_enabled("hedis_summary", cfg_pro), "FAIL: PRO hedis_summary"
assert is_feature_enabled("hedis_predictions", cfg_pro), "FAIL: PRO hedis_predictions"

print("✅ hedis_summary — FREE tier confirmed")
print("✅ hedis_predictions — PRO tier confirmed")
print("✅ hedis flags live — free summary / pro predictions")
