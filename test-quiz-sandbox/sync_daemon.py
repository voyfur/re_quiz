#!/usr/bin/env python3
"""Scheduled Background Sync Daemon for Race Expert Quiz Catalog.

Runs periodically to fetch changes from OpenCart and enrich new kits via AI.
"""

import sys
import time
import signal
import logging
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from catalog_sync_pipeline import run_sync

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [SYNC_DAEMON] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("sync_daemon")

_RUNNING = True

def _handle_exit(sig, frame):
    global _RUNNING
    logger.info(f"Received exit signal ({sig}). Stopping daemon cleanly...")
    _RUNNING = False

signal.signal(signal.SIGINT, _handle_exit)
signal.signal(signal.SIGTERM, _handle_exit)


def main():
    parser = argparse.ArgumentParser(description="Race Expert Catalog Sync Daemon")
    parser.add_argument("--interval", type=int, default=86400, help="Interval between sync runs in seconds (default 86400 = 24h)")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode")
    parser.add_argument("--dry-run", action="store_true", help="Run without persisting changes")
    parser.add_argument("--run-once", action="store_true", help="Run single sync and exit immediately")
    args = parser.parse_args()

    logger.info(f"Sync daemon initialized (interval={args.interval}s, mock={args.mock}, dry_run={args.dry_run})")

    while _RUNNING:
        try:
            logger.info("Executing scheduled catalog synchronization...")
            report = run_sync(mock=args.mock, dry_run=args.dry_run, use_llm=True)
            logger.info(f"Sync result: {report.get('status')} | New: {report.get('new_kits_added')} | Prices: {report.get('prices_updated')}")
        except Exception as e:
            logger.error(f"Error during synchronization run: {e}", exc_info=True)

        if args.run_once:
            break

        # Sleep in small slices to respond promptly to termination signals
        slept = 0
        while _RUNNING and slept < args.interval:
            time.sleep(min(5, args.interval - slept))
            slept += 5

    logger.info("Sync daemon terminated.")


if __name__ == "__main__":
    main()
