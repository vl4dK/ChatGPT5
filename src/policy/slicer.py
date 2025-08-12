from __future__ import annotations
import random, time
from dataclasses import dataclass

@dataclass
class SlicerConfig:
    aggressiveness: float = 0.3  # 0..1
    randomize_ms_min: int = 200
    randomize_ms_max: int = 1200

class OrderSlicer:
    """TWAP-like child order scheduler with randomization and post-only preference."""
    def __init__(self, cfg: SlicerConfig | None = None):
        self.cfg = cfg or SlicerConfig()

    def child_delaysec(self) -> float:
        jitter_ms = random.randint(self.cfg.randomize_ms_min, self.cfg.randomize_ms_max)
        return max(0.05, jitter_ms / 1000.0 * (0.6 + 0.8*self.cfg.aggressiveness))

    def next_child_qty(self, parent_qty: float) -> float:
        # Smaller slices for low aggressiveness
        base = parent_qty * (0.1 + 0.3*self.cfg.aggressiveness)
        return max(base, parent_qty * 0.02)
