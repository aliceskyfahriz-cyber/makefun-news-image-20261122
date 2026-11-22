#!/bin/sh
# Build the 22 November 2026 news image and place a copy at /output/entry.png.
set -e
cd "$(dirname "$0")"
python3 main.py
mkdir -p /output 2>/dev/null && cp output.png /output/entry.png 2>/dev/null || true
