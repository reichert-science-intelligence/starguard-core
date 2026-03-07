"""
Phase 4 auth/tier — API key validation, feature flags, usage tracking.
"""
from starguard_core.auth.tiers import Tier
from starguard_core.auth.validator import (
    UPGRADE_URL,
    capture_lead,
    get_tier_config,
    get_usage_count,
    increment_usage,
    is_feature_enabled,
    validate_api_key,
)

__all__ = [
    "Tier",
    "UPGRADE_URL",
    "capture_lead",
    "get_tier_config",
    "get_usage_count",
    "increment_usage",
    "is_feature_enabled",
    "validate_api_key",
]
