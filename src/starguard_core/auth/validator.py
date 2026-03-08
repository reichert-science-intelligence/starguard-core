"""
API key validation, feature flags, usage tracking.
Test keys: pro-TESTKEY0000000001 -> PRO, None/empty -> FREE.
"""
from dataclasses import dataclass
from typing import Any

from starguard_core.auth.tiers import Tier

UPGRADE_URL = "https://reichert-science-intelligence.github.io/starguard-core/upgrade"

# In-memory usage store (per process; for demo/testing)
_usage: dict[tuple[str | None, str], int] = {}

# Feature -> tier mapping (PRO gets hedis_predictions, radv_calculator, hcc_scoring, stars_calculator)
_FEATURE_TIERS: dict[str, set[Tier]] = {
    "hedis_summary": {Tier.FREE, Tier.PRO},  # Week 4: FREE summary, PRO predictions
    "hedis_predictions": {Tier.PRO},
    "radv_calculator": {Tier.PRO},  # Week 2: radv_calculator now Pro-tier
    "hcc_scoring": {Tier.PRO},      # Week 3: RAF calculator, gaps, revenue, compound view
    "stars_calculator": {Tier.PRO},  # Week 5: QBP threshold, trajectory, command center
}


def _resolve_tier(api_key: str | None) -> Tier:
    """Resolve API key to tier."""
    if not api_key or not api_key.strip():
        return Tier.FREE
    key = api_key.strip()
    if key.startswith("pro-") and len(key) >= 20:
        return Tier.PRO
    return Tier.FREE


@dataclass
class MemberRecord:
    """Result of validate_api_key."""

    tier: Tier
    api_key: str | None
    is_valid: bool


def validate_api_key(api_key: str | None) -> MemberRecord:
    """Validate API key and return tier. None -> FREE, pro-TESTKEY... -> PRO."""
    tier = _resolve_tier(api_key)
    is_valid = tier != Tier.FREE or api_key is None
    return MemberRecord(tier=tier, api_key=api_key, is_valid=is_valid)


def get_tier_config(api_key: str | None) -> dict[str, Any]:
    """Return tier config dict for is_feature_enabled."""
    tier = _resolve_tier(api_key)
    return {"tier": tier}


def is_feature_enabled(feature: str, tier_config: dict[str, Any]) -> bool:
    """Check if feature is enabled for given tier config."""
    tier = tier_config.get("tier", Tier.FREE)
    allowed = _FEATURE_TIERS.get(feature, set())
    return tier in allowed


def increment_usage(api_key: str | None, feature: str, app_name: str) -> None:
    """Increment usage count for api_key + feature."""
    k = (api_key or "", feature)
    _usage[k] = _usage.get(k, 0) + 1


def get_usage_count(api_key: str | None, feature: str) -> int:
    """Return usage count for api_key + feature."""
    k = (api_key or "", feature)
    return _usage.get(k, 0)


def capture_lead(email: str, source: str = "web") -> None:
    """Capture lead (no-op for now)."""
    pass
