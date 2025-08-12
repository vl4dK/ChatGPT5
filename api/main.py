from __future__ import annotations
import threading, time, queue
from typing import Optional, Dict, Any, List
from fastapi import FastAPI
from pydantic import BaseModel
from src.orchestration.service import BotService, BotConfig

app = FastAPI(title="ML Trading Bot API", version="0.1.0")

# Singleton bot service
bot_service = BotService()

class StartRequest(BaseModel):
    paper: bool = True

@app.get("/status")
def status():
    s = bot_service.status()
    return s

@app.post("/start")
def start(req: StartRequest):
    bot_service.start(paper=req.paper)
    return {"ok": True, "running": True, "paper": req.paper}

@app.post("/stop")
def stop():
    bot_service.stop()
    return {"ok": True, "running": False}

@app.get("/positions")
def positions():
    return bot_service.get_positions()

@app.get("/orders")
def orders():
    return bot_service.get_orders()

@app.get("/trades")
def trades():
    return bot_service.get_trades()

@app.get("/metrics")
def metrics():
    return bot_service.get_metrics()
