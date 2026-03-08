# verify_stars_flags.py
"""Verify Stars feature flag: PRO gets stars_calculator."""
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from starguard_core.auth.validator import get_tier_config, is_feature_enabled

cfg_free = get_tier_config(None)
cfg_pro = get_tier_config("pro-TESTKEY0000000001")

assert not is_feature_enabled("stars_calculator", cfg_free), "FAIL: FREE stars_calculator"
assert is_feature_enabled("stars_calculator", cfg_pro), "FAIL: PRO stars_calculator"

print("[OK] stars_calculator - PRO tier confirmed")
print("[OK] stars flags live - Week 5")
