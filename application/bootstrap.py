from __future__ import annotations
from domain.pricing import PricingStrategy, NoDiscount, PercentageDiscount, BulkItemDiscount, CompositeStrategy, MinimumOrderDiscountStrategy


def choose_strategy(kind: str, **kwargs) -> PricingStrategy:
    kind = kind.lower()
    if kind == "none":
        return NoDiscount()
    if kind == "percent":
        return PercentageDiscount(kwargs.get("percent", 0.0))
    if kind == "bulk":
        return BulkItemDiscount(
            sku=kwargs.get("sku", ""),
            threshold=int(kwargs.get("threshold", 0)),
            per_item_off=float(kwargs.get("per_item_off", 0.0)),
        )
    if kind == "minimum":
        return MinimumOrderDiscountStrategy(
            min_amount=float(kwargs.get("min_amount", 0.0)),
            discount_percent=float(kwargs.get("discount_percent", 0.0)),
        )
    if kind == "composite":
        # Example: combine percent then bulk
        percent = PercentageDiscount(kwargs.get("percent", 0.0))
        bulk = BulkItemDiscount(
            sku=kwargs.get("sku", ""),
            threshold=int(kwargs.get("threshold", 0)),
            per_item_off=float(kwargs.get("per_item_off", 0.0)),
        )
        return CompositeStrategy([percent, bulk])
    raise ValueError(f"Unknown strategy kind: {kind}")
