from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass
class ImpactParams:
    max_impact_bps: float = 8.0   # hard cap on expected impact per trade (basis points)
    child_max_notional_bps: float = 50.0  # child order size as bps of visible top-of-book notional

class ImpactModel:
    """Simple slippage/impact bands by volatility & liquidity buckets.
    Replace with calibrated model from fills & order book analytics.
    """
    def __init__(self, params: ImpactParams | None = None):
        self.params = params or ImpactParams()

    def expected_slippage_bps(self, vol_bucket: str, liq_bucket: str, aggressiveness: float) -> float:
        base = {
            ("low","high"): 0.5,
            ("low","mid"): 1.0,
            ("mid","mid"): 1.5,
            ("mid","low"): 2.5,
            ("high","low"): 4.0,
        }.get((vol_bucket, liq_bucket), 2.0)
        # scale by aggressiveness [0..1]
        return min(base * (0.6 + 0.8*aggressiveness), self.params.max_impact_bps)

    def child_size_limit_bps(self) -> float:
        return self.params.child_max_notional_bps
