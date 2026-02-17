#!/bin/bash

# Ensure virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

# run the examples
python examples.py
