#!/usr/bin/env python3
"""
Smart Troubleshooting Expert System — application entry point.

Run from this directory:
    python main.py

The package root is added to sys.path so imports resolve without installation.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from expert_system.presentation.app import launch_app

if __name__ == "__main__":
    launch_app()
