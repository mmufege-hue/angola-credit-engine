@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m streamlit run app.py
) else if exist "..\.venv\Scripts\python.exe" (
    "..\.venv\Scripts\python.exe" -m streamlit run app.py
) else (
    where py >nul 2>&1
    if errorlevel 1 (
        echo Python Launcher was not found. Install Python 3.11+ and project dependencies.
        goto startup_error
    )
    py -3 -m streamlit run app.py
)

if errorlevel 1 goto startup_error
exit /b 0

:startup_error
echo.
echo Startup failed. Install dependencies with: python -m pip install -r requirements.txt
echo If Windows blocks Python DLLs or project writes, move this folder outside .vscode or ask IT to allow the trusted Python environment.
pause
exit /b 1
