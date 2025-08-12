from __future__ import annotations
import time, hmac, hashlib, json, requests
from typing import Any, Dict, List, Optional

class HyperliquidClient:
    """Minimal HTTP client stub for Hyperliquid-like REST API.
    Replace endpoints and signing with the official SDK when available.
    """
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.hyperliquid.xyz"):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.base_url = base_url.rstrip('/')

    def _sign(self, payload: str) -> str:
        return hmac.new(self.api_secret, payload.encode(), hashlib.sha256).hexdigest()

    def _headers(self, payload: str) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
            "X-SIGNATURE": self._sign(payload),
        }

    def _request(self, method: str, path: str, data: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{path}"
        payload = json.dumps(data or {})
        resp = requests.request(method, url, headers=self._headers(payload), data=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()

    # ---- Public-like helpers ----
    def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 500) -> List[List[Any]]:
        # Placeholder; adjust to Hyperliquid's actual market data endpoint
        return []

    # ---- Private endpoints ----
    def place_order(self, symbol: str, side: str, qty: float, price: Optional[float] = None, type_: str = "limit", post_only: bool = True) -> Dict[str, Any]:
        data = {"symbol": symbol, "side": side, "qty": qty, "type": type_, "price": price, "postOnly": post_only}
        return {"status": "stub", "order": data}

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        return {"status": "stub", "order_id": order_id}

    def fetch_positions(self) -> List[Dict[str, Any]]:
        return []

    def fetch_open_orders(self) -> List[Dict[str, Any]]:
        return []
