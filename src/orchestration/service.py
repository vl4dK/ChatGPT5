from __future__ import annotations
import threading, time, queue, random, datetime as dt
from typing import Dict, Any, List
from dataclasses import dataclass, field

from src.models.engine import DecisionEngine
from src.policy.impact_model import ImpactModel, ImpactParams
from src.policy.toxicity import ToxicityMeter
from src.policy.slicer import OrderSlicer, SlicerConfig

from src.policy.toxicity import ToxicityModel

@dataclass
class BotConfig:
    timeframe_primary: str = "1h"
    timeframe_secondary: str = "4h"

class BotService:
    def __init__(self):
        self._thread = None
        self._running = False
        self._paper = True
        self._lock = threading.Lock()
        self._orders: List[dict] = []
        self._trades: List[dict] = []
        self._positions: Dict[str, dict] = {}
        self._metrics: Dict[str, float] = {"pnl": 0.0, "sharpe": 0.0, "asr": 0.0}
        self._engine = DecisionEngine()
        self._impact = ImpactModel()
        self._tox = ToxicityMeter()
        self._slicer = OrderSlicer()
        self._toxicity = ToxicityModel()
        self._cfg = BotConfig()

    def _loop(self):
        # Simplified loop: every minute emulate decision; in real code use bar-close triggers
        while self._running:
            now = dt.datetime.utcnow()
            # Simulate decision
            decision = self._engine.decide()
            if decision.get("action") in ("BUY", "SELL"):
                symbol = decision.get("symbol", "BTC/USDT")
                qty = decision.get("qty", 0.001)
                price = decision.get("price", 0.0)
                order = {"ts": now.isoformat(), "symbol": symbol, "side": decision["action"], "qty": qty, "price": price, "paper": self._paper}
                self._orders.append(order)
                # Simulate fill
                self._trades.append({**order, "fill_price": price, "fee": 0.0})
                # Update toxicity (demo: mid_after = price +/- small drift)
                mid_after = price * (1.0 + (0.0005 if decision["action"]=="BUY" else -0.0005))
                self._tox.record_fill(decision["action"], price, mid_after)
                # Update PnL (dummy)
                self._metrics["pnl"] += random.uniform(-2, 2)
                self._metrics["asr"] = self._tox.asr
            
            # Record fake ASR
            mid_before = price
            mid_after = price + random.uniform(-10, 10)
            self._toxicity.record(mid_before, mid_after, decision.get("action", ""))
time.sleep(60)

    def start(self, paper: bool = True):
        with self._lock:
            if self._running:
                return
            self._paper = paper
            self._running = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        with self._lock:
            self._running = False
            th = self._thread
        if th:
            th.join(timeout=0.1)

    def status(self) -> dict:
        return {
            "running": self._running,
            "paper": self._paper,
            "pnl": self._metrics.get("pnl", 0.0),
            "orders": len(self._orders),
            "trades": len(self._trades),
            "asr": self._toxicity.asr,
            "positions": len(self._positions),
        }

    def get_positions(self) -> dict:
        return self._positions

    def get_orders(self) -> list:
        return self._orders[-200:]

    def get_trades(self) -> list:
        return self._trades[-200:]

    def get_metrics(self) -> dict:
        return self._metrics
