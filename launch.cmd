@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run setup.cmd first.
  exit /b 1
)
".venv\Scripts\python.exe" launcher.py %*
