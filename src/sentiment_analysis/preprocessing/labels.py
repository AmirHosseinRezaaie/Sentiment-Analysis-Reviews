"""Shared rating validation and binary sentiment-label helpers."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any


def normalize_rating(value: Any) -> int | None:
    """Normalize a five-star rating; invalid and missing values stay unknown."""
    try:
        numeric_rating = Decimal(str(value).strip())
    except (InvalidOperation, TypeError, ValueError):
        return None
    if not numeric_rating.is_finite() or numeric_rating != numeric_rating.to_integral_value():
        return None
    rating = int(numeric_rating)
    return rating if 1 <= rating <= 5 else None


def sentiment_from_rating(value: Any) -> int | None:
    """Map 1-2 stars to negative and 4-5 to positive; exclude neutral/invalid."""
    rating = normalize_rating(value)
    if rating in (1, 2):
        return 0
    if rating in (4, 5):
        return 1
    return None
