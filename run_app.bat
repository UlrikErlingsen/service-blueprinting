@echo off
setlocal
cd /d "%~dp0"
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
  echo Blueprint Signal needs Python 3.10 or newer.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo Creating Blueprint Signal's private Python environment...
  py -m venv .venv
)
".venv\Scripts\python.exe" -c "import streamlit, plotly, openpyxl, jsonschema" >nul 2>&1
if errorlevel 1 (
  echo Installing Blueprint Signal's open-source packages...
  ".venv\Scripts\python.exe" -m pip --disable-pip-version-check install --prefer-binary -r requirements.txt
  if errorlevel 1 (
    pause
    exit /b 1
  )
)
if not defined ARROW_DEFAULT_MEMORY_POOL set ARROW_DEFAULT_MEMORY_POOL=system
if "%BLUEPRINTSIGNAL_PORT%"=="" set BLUEPRINTSIGNAL_PORT=8602
if "%BLUEPRINTSIGNAL_MAX_UPLOAD_MB%"=="" set BLUEPRINTSIGNAL_MAX_UPLOAD_MB=50
echo Starting Blueprint Signal at http://127.0.0.1:%BLUEPRINTSIGNAL_PORT% ...
".venv\Scripts\python.exe" -m streamlit run app.py --server.headless=true --server.address=127.0.0.1 --server.port=%BLUEPRINTSIGNAL_PORT% --server.maxUploadSize=%BLUEPRINTSIGNAL_MAX_UPLOAD_MB% --server.fileWatcherType=none --browser.gatherUsageStats=false
if errorlevel 1 pause
