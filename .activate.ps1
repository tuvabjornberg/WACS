# Powershell script for venv setup and activation

Write-Host "ACTIVATING WACS" 

$VENV_NAME = ".venv"
$REQ_FILE = "requirements.txt"

if (-Not (Test-Path $VENV_NAME)) {
    Write-Output "Python environment setup"
    python -m venv $VENV_NAME
    & "$VENV_NAME\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
    if (Test-Path $REQ_FILE) {
        & "$VENV_NAME\Scripts\python.exe" -m pip install -r $REQ_FILE
    }
}

# Update packages if requirements.txt is modified
if (Test-Path $REQ_FILE) {
    Write-Output "Updating packages from requirements.txt"
    & "$VENV_NAME\Scripts\python.exe" -m pip install -r $REQ_FILE
}

# Activate venv
& "$VENV_NAME\Scripts\Activate.ps1"
python --version
