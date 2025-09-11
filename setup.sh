#!/bin/bash

if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Removing it and creating a new one."
    rm -rf .venv
fi

echo "Creating virtual environment in .venv directory..."
python3 -m venv .venv

if [ ! -d ".venv" ]; then
    echo "Error: Failed to create virtual environment."
    echo "Please ensure Python 3 is installed and in your PATH."
    exit 1
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
python3 -m pip install .

if [ $? -eq 0 ]; then
    echo "================================================"
    echo "Setup complete! Please run the following command to activate your environment:"
    echo "source .venv/bin/activate"
    echo "================================================"
else
    echo "Error: Failed to install dependencies."
    echo "Please check the error messages above."
fi