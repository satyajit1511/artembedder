#!/bin/bash

# Ensure we are in the directory where the script is located
cd "$(dirname "$0")"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

# Run the application
# We use python3 explicitly for Linux compatibility
python3 main.py "$@"
