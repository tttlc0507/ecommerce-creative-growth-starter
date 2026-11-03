#!/usr/bin/env python3
"""Run the local metrics helper shipped inside the installable skill."""
import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "skills/ecommerce-creative-growth-starter/scripts/metrics.py"), run_name="__main__")
