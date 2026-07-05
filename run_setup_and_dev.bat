@echo off
title CricSQL Control Center
cls
echo ======================================================================
echo              CricSQL AI Analytics Platform Control Center
echo ======================================================================
echo.
echo Please select an action to perform:
echo  [1] Start Developer Servers Only (FastAPI backend + Vite frontend)
echo  [2] Run Data Ingestion (Import datasets into MySQL)
echo  [3] Run Full Project Setup (Install dependencies, import datasets, start servers)
echo  [4] Run Backend Test Suite (FastAPI + SQL validation + Auth tests)
echo  [5] Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto start_servers
if "%choice%"=="2" goto run_ingestion
if "%choice%"=="3" goto run_setup
if "%choice%"=="4" goto run_tests
if "%choice%"=="5" exit
goto invalid_choice

:run_setup
echo.
echo ======================================================================
echo [1/3] Installing Python backend dependencies...
echo ======================================================================
pip install -r backend/requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install python packages. Make sure Python is in your PATH.
    pause
    goto start_servers
)

echo.
echo ======================================================================
echo [2/3] Ingesting CSV datasets into MySQL ipl_ai database...
echo ======================================================================
python backend/import_data.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to run import_data.py. Make sure MySQL service is running.
    pause
    goto start_servers
)

echo.
echo ======================================================================
echo [3/3] Installing Node.js frontend dependencies...
echo ======================================================================
cd frontend
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to run npm install. Make sure Node.js is installed.
    cd ..
    pause
    goto start_servers
)
cd ..
echo.
echo [SUCCESS] CricSQL Full Initialization Complete!
echo.
goto start_servers

:run_ingestion
echo.
echo ======================================================================
echo Running dataset ingestion to MySQL ipl_ai...
echo ======================================================================
python backend/import_data.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ingestion failed. Make sure MySQL is running.
) else (
    echo [SUCCESS] Data ingested successfully!
)
pause
cls
goto :EOF

:start_servers
echo.
echo ======================================================================
echo Launching CricSQL Dev Servers...
echo ======================================================================
echo.
echo [INFO] Starting FastAPI Backend on http://localhost:8000
start "CricSQL Backend Server" cmd /k "title CricSQL Backend && uvicorn backend.app.main:app --reload --port 8000"

echo [INFO] Starting Vite Frontend on http://localhost:5173
start "CricSQL Frontend Server" cmd /k "title CricSQL Frontend && cd frontend && npm run dev"

echo.
echo ======================================================================
echo Servers have been launched in separate terminal windows!
echo - You can view the frontend at http://localhost:5173
echo - You can view API documentation at http://localhost:8000/docs
echo ======================================================================
echo.
pause
exit

:run_tests
echo.
echo ======================================================================
echo Running CricSQL Backend Test Suite...
echo ======================================================================
python backend/tests/run_tests.py
pause
cls
goto :EOF

:invalid_choice
echo.
echo [ERROR] Invalid choice. Please select a number between 1 and 4.
pause
cls
goto :EOF
