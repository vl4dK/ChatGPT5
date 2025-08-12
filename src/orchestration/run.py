from __future__ import annotations
import argparse, os, time, datetime as dt
from dotenv import load_dotenv

# Stubs to simulate scheduling; replace with Prefect flows later.
def daily_retrain():
    print("➡️  Running daily retrain pipeline (stub)...")
    time.sleep(0.2)
    print("✅ Retrain complete (stub).")

def live_decisions():
    now = dt.datetime.now().isoformat(timespec="seconds")
    print(f"➡️  Making live decisions at {now} (stub)...")
    time.sleep(0.2)
    print("✅ Decisions done (stub).")

def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--flow", required=True, choices=["daily_retrain", "live_decisions"])
    args = parser.parse_args()
    if args.flow == "daily_retrain":
        daily_retrain()
    elif args.flow == "live_decisions":
        live_decisions()

if __name__ == "__main__":
    main()
