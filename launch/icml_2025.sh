#!/bin/bash

# Launch crawler for ICML 2025

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Ensure virtual environment exists
if [ ! -d "$ROOT_DIR/venv" ]; then
    echo "Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate the virtual environment
source "$ROOT_DIR/venv/bin/activate"

# Run the crawler for ICML 2025
python "$ROOT_DIR/crawl.py" --conference ICML2025 --limit 50
