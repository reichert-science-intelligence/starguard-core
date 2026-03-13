"""Auth module tests — covers Tier, validate_api_key, feature flags, usage tracking."""
from starguard_core.auth.tiers import Tier
from starguard_core.auth.validator import (
    UPGRADE_URL,
    MemberRecord,
    capture_lead,
    get_tier_config,
    get_usage_count,
    increment_usage,
    is_feature_enabled,
    validate_api_key,
)
from starguard_core.auth import (
    Tier as AuthTier,
    validate_api_key as auth_validate,
    is_feature_enabled as auth_feature,
)


# --- tiers ---
def test_tier_free_value():
    """Tier.FREE has value 'free'."""
    assert Tier.FREE.value == "free"


def test_tier_pro_value():
    """Tier.PRO has value 'pro'."""
    assert Tier.PRO.value == "pro"


def test_tier_is_str_enum():
    """Tier is a str enum — can compare to string."""
    assert Tier.FREE == "free"
    assert Tier.PRO == "pro"


# --- validate_api_key ---
def test_validate_api_key_none_returns_free():
    """None key resolves to FREE tier."""
    rec = validate_api_key(None)
    assert isinstance(rec, MemberRecord)
    assert rec.tier == Tier.FREE
    assert rec.is_valid is True


def test_validate_api_key_empty_returns_free():
    """Empty string key resolves to FREE tier."""
    rec = validate_api_key("")
    assert rec.tier == Tier.FREE


def test_validate_api_key_whitespace_returns_free():
    """Whitespace-only key resolves to FREE tier."""
    rec = validate_api_key("   ")
    assert rec.tier == Tier.FREE


def test_validate_api_key_pro_prefix_long_returns_pro():
    """Key starting with 'pro-' and length >= 20 resolves to PRO."""
    rec = validate_api_key("pro-TESTKEY0000000001")
    assert rec.tier == Tier.PRO


def test_validate_api_key_pro_prefix_short_returns_free():
    """Key starting with 'pro-' but length < 20 resolves to FREE."""
    rec = validate_api_key("pro-SHORT")
    assert rec.tier == Tier.FREE


def test_validate_api_key_non_pro_returns_free():
    """Arbitrary non-pro key resolves to FREE tier."""
    rec = validate_api_key("basic-key-12345")
    assert rec.tier == Tier.FREE


def test_validate_api_key_stores_api_key():
    """MemberRecord stores the original api_key."""
    rec = validate_api_key("pro-TESTKEY0000000001")
    assert rec.api_key == "pro-TESTKEY0000000001"


# --- get_tier_config ---
def test_get_tier_config_none_is_free():
    """get_tier_config(None) returns FREE tier config."""
    cfg = get_tier_config(None)
    assert cfg["tier"] == Tier.FREE


def test_get_tier_config_pro_key_is_pro():
    """get_tier_config with pro key returns PRO tier config."""
    cfg = get_tier_config("pro-TESTKEY0000000001")
    assert cfg["tier"] == Tier.PRO


# --- is_feature_enabled ---
def test_is_feature_enabled_hedis_summary_free():
    """hedis_summary is enabled for FREE tier."""
    cfg = get_tier_config(None)
    assert is_feature_enabled("hedis_summary", cfg) is True


def test_is_feature_enabled_hedis_predictions_free_denied():
    """hedis_predictions is NOT enabled for FREE tier."""
    cfg = get_tier_config(None)
    assert is_feature_enabled("hedis_predictions", cfg) is False


def test_is_feature_enabled_hedis_predictions_pro():
    """hedis_predictions is enabled for PRO tier."""
    cfg = get_tier_config("pro-TESTKEY0000000001")
    assert is_feature_enabled("hedis_predictions", cfg) is True


def test_is_feature_enabled_radv_calculator_pro():
    """radv_calculator is enabled for PRO tier."""
    cfg = get_tier_config("pro-TESTKEY0000000001")
    assert is_feature_enabled("radv_calculator", cfg) is True


def test_is_feature_enabled_hcc_scoring_pro():
    """hcc_scoring is enabled for PRO tier."""
    cfg = get_tier_config("pro-TESTKEY0000000001")
    assert is_feature_enabled("hcc_scoring", cfg) is True


def test_is_feature_enabled_stars_calculator_pro():
    """stars_calculator is enabled for PRO tier."""
    cfg = get_tier_config("pro-TESTKEY0000000001")
    assert is_feature_enabled("stars_calculator", cfg) is True


def test_is_feature_enabled_unknown_feature_returns_false():
    """Unknown feature returns False for any tier."""
    cfg = get_tier_config("pro-TESTKEY0000000001")
    assert is_feature_enabled("nonexistent_feature", cfg) is False


# --- usage tracking ---
def test_get_usage_count_zero_initially():
    """Usage count is 0 before any increments for unique key."""
    count = get_usage_count("unique-key-xyz", "hedis_summary")
    assert count == 0


def test_increment_and_get_usage_count():
    """increment_usage + get_usage_count tracks correctly."""
    increment_usage("test-key-001", "radv_calculator", "app")
    increment_usage("test-key-001", "radv_calculator", "app")
    assert get_usage_count("test-key-001", "radv_calculator") == 2


def test_usage_count_none_key():
    """Usage tracking works with None api_key."""
    increment_usage(None, "hedis_summary", "app")
    count = get_usage_count(None, "hedis_summary")
    assert count >= 1


def test_usage_count_independent_per_feature():
    """Usage counts are tracked independently per feature."""
    increment_usage("key-abc", "hcc_scoring", "app")
    stars_count = get_usage_count("key-abc", "stars_calculator")
    assert stars_count == 0


# --- capture_lead ---
def test_capture_lead_no_op():
    """capture_lead is a no-op and returns None."""
    result = capture_lead("user@example.com")
    assert result is None


def test_capture_lead_with_source():
    """capture_lead accepts source parameter without error."""
    result = capture_lead("user@example.com", source="mobile")
    assert result is None


# --- upgrade url ---
def test_upgrade_url_defined():
    """UPGRADE_URL is a non-empty string."""
    assert isinstance(UPGRADE_URL, str)
    assert len(UPGRADE_URL) > 0


# --- __init__ re-exports ---
def test_auth_module_re_exports_tier():
    """starguard_core.auth re-exports Tier."""
    assert AuthTier.FREE == Tier.FREE
    assert AuthTier.PRO == Tier.PRO


def test_auth_module_re_exports_validate():
    """starguard_core.auth re-exports validate_api_key."""
    rec = auth_validate("pro-TESTKEY0000000001")
    assert rec.tier == Tier.PRO


def test_auth_module_re_exports_is_feature_enabled():
    """starguard_core.auth re-exports is_feature_enabled."""
    cfg = {"tier": Tier.PRO}
    assert auth_feature("radv_calculator", cfg) is True
