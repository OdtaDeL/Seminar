<#
Setup helper for Windows (PowerShell).
Run from repository root:
  powershell -ExecutionPolicy RemoteSigned -File .\scripts\setup_windows.ps1

What it does:
 - Optionally remove a committed `venv/` from git index
 - Create a new virtual environment `venv`
 - Activate the venv in the script and install `requirements.txt`
 - Print next-step commands
#>

Write-Host "=== Seminar project Windows setup script ==="

if (Test-Path .\venv) {
    Write-Host "Found existing 'venv' directory."
    Write-Host "If this was committed to git, it's recommended to remove it from the index."
    if (Get-Command git -ErrorAction SilentlyContinue) {
        Write-Host "Removing venv from git index (git rm --cached -r venv)..."
        git rm -r --cached venv 2>$null
    } else {
        Write-Host "git not found in PATH; skipping git rm step."
    }
}

Write-Host "Creating virtual environment 'venv'..."
python -m venv venv

Write-Host "Activating venv (this activation lasts for the duration of this script)..."
& .\venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..."
pip install --upgrade pip

Write-Host "Installing requirements from requirements.txt (this may take a few minutes)..."
pip install -r requirements.txt

Write-Host "\nSetup finished. Quick commands for you:\n"
Write-Host "Activate venv (in a new PowerShell session):"
Write-Host ".\venv\Scripts\Activate.ps1\n"
Write-Host "Run tests:"
Write-Host "python src/test_10_cases.py"
Write-Host "python src/test_improved.py\n"
Write-Host "Run Streamlit app:"
Write-Host "streamlit run src/app.py\n"

Write-Host "If you get an execution policy error when activating, run once as admin or set per-user:\n"
Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
