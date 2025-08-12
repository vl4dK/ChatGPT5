from __future__ import annotations
import random
from dataclasses import dataclass

@dataclass
class StressConfig:
    extra_spread_bps: float = 1.5
    extra_slippage_bps: float = 2.0
    early_competitor: bool = True  # someone similar trades 1 bar earlier

class StressExecution:
    """Applies pessimistic adjustments to fills to simulate competition."""
    def __init__(self, cfg: StressConfig | None = None):
        self.cfg = cfg or StressConfig()

    def apply(self, price: float, side: str) -> float:
        drift = self.cfg.extra_slippage_bps / 10000.0 * price
        spread = self.cfg.extra_spread_bps / 10000.0 * price
        sign = 1 if side == "BUY" else -1
        return price + sign * (drift + spread)
