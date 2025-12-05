<#
Run helper for Windows (PowerShell).
Usage:
  .\scripts\run_windows.ps1 start   # start Streamlit app
  .\scripts\run_windows.ps1 test    # run pytest on tests/
  .\scripts\run_windows.ps1 both    # run tests then start app

This script expects you to have created and activated the venv, or it will create one.
#>

param(
    [string]$action = "start"
)

function Ensure-Venv {
    if (-not (Test-Path .\venv)) {
        Write-Host "Creating virtual environment..."
        python -m venv venv
    }
}

function Activate-Venv {
    .\venv\Scripts\Activate.ps1
}

switch ($action.ToLower()) {
    'test' {
        Ensure-Venv
        Activate-Venv
        pip install --upgrade pip
        pip install -r requirements.txt
        Write-Host "Running pytest..."
        python -m pytest tests -q
        break
    }
    'both' {
        Ensure-Venv
        Activate-Venv
        pip install --upgrade pip
        pip install -r requirements.txt
        Write-Host "Running pytest..."
        python -m pytest tests -q
        Write-Host "Starting Streamlit app..."
        streamlit run src/app.py
        break
    }
    default {
        Ensure-Venv
        Activate-Venv
        pip install --upgrade pip
        pip install -r requirements.txt
        Write-Host "Starting Streamlit app..."
        streamlit run src/app.py
    }
}
