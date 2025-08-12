from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ExecAttribution:
    spread_loss: float = 0.0
    queue_loss: float = 0.0
    impact_loss: float = 0.0

def asr_from_fills(fills):
    if not fills: 
        return 0.0
    adverse = sum(int(f.get("adverse", False)) for f in fills)
    return adverse / max(1, len(fills))
