from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict

@dataclass
class ToxicityState:
    window: int = 50  # track last N fills
    adverse_after_ms: int = 3000

class ToxicityMeter:
    """Tracks Adverse Selection Rate (ASR) proxy from recent fills and midprice moves."""
    def __init__(self, state: ToxicityState | None = None):
        self.state = state or ToxicityState()
        self.events: Deque[Dict] = deque(maxlen=self.state.window)
        self.asr: float = 0.0  # 0..1

    def record_fill(self, side: str, fill_price: float, mid_after: float):
        adverse = (side == "BUY" and mid_after < fill_price) or (side == "SELL" and mid_after > fill_price)
        self.events.append({"adverse": adverse})
        if self.events:
            self.asr = sum(int(e["adverse"]) for e in self.events) / len(self.events)

    def should_cut_size(self, threshold: float = 0.55) -> bool:
        return self.asr >= threshold
