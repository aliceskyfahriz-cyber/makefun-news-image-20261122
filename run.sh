#!/bin/sh
# Build the 22 November 2026 news image and place a copy at /output/entry.png.
set -e
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
    PY=python3
else
    PY=python
fi
$PY main.py
mkdir -p /output 2>/dev/null && cp output.png /output/entry.png 2>/dev/null || true
