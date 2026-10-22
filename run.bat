@echo off
REM Double-click to start the dashboard. First run sets everything up (needs internet).
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed. Get it from https://www.python.org/downloads/
    echo During install, tick "Add Python to PATH". Then run this file again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo First run: setting up, this takes a few minutes...
    python -m venv .venv || goto :error
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt || goto :error
)

if not exist "social_media_screentime_mental_health_2026.csv" (
    echo No dataset found, creating sample data...
    ".venv\Scripts\python.exe" make_sample_data.py
)

echo Starting dashboard at http://localhost:8501  (close this window to stop)
".venv\Scripts\python.exe" -m streamlit run app.py
pause
exit /b 0

:error
echo Setup failed. Check your internet connection, delete the .venv folder and try again.
pause
exit /b 1
