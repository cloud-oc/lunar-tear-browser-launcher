param([string]$Python = '')
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Test-Path '.venv\Scripts\python.exe')) {
    if ($Python) {
        & $Python -c "import sys; assert sys.version_info >= (3,10), 'Python 3.10+ required'"
        if ($LASTEXITCODE -ne 0) { throw 'Python 3.10+ required' }
        & $Python -m venv .venv
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 -c "import sys; assert sys.version_info >= (3,10), 'Python 3.10+ required'"
        if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.10+ from python.org, then retry.' }
        & py -3 -m venv .venv
    } else {
        & python -c "import sys; assert sys.version_info >= (3,10), 'Python 3.10+ required'"
        if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.10+ from python.org, then retry.' }
        & python -m venv .venv
    }
    if ($LASTEXITCODE -ne 0) { throw 'Failed to create virtual environment' }
}
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
& .\.venv\Scripts\python.exe launcher.py init
Write-Host 'Setup complete. Edit config.json, then follow README.md for first-time game preparation.'
