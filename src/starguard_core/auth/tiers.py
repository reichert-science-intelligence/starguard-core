"""Tier enum for API key validation."""
from enum import Enum


class Tier(str, Enum):
    """Subscription tier."""

    FREE = "free"
    PRO = "pro"
