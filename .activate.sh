#!/bin/bash
Write-Host "ACTIVATING WACS" 

VENV_NAME=".venv"
REQ_FILE="requirements.txt"

if [ ! -d "$VENV_NAME" ]; then
    echo "Setting up Python virtual environment"
    python3 -m venv $VENV_NAME
    source $VENV_NAME/bin/activate
    pip install --upgrade pip setuptools wheel
    if [ -f "$REQ_FILE" ]; then
        pip install -r $REQ_FILE
    fi
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment"
source $VENV_NAME/bin/activate
python3 --version
