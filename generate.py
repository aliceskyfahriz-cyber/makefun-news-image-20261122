#!/usr/bin/env python3
"""Thin wrapper: run the entry builder (see main.py)."""

import runpy
import os

HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    runpy.run_path(os.path.join(HERE, "main.py"), run_name="__main__")
