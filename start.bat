@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal EnableExtensions EnableDelayedExpansion
start "Generated API server" /min "%ComSpec%" /c ""%~dp0api\start_server.bat""
timeout /t 2 /nobreak >nul
where py >nul 2>nul
if not errorlevel 1 (
    py -3 main.py
    set "APP_EXIT=!errorlevel!"
    goto :done
)
where python >nul 2>nul
if not errorlevel 1 (
    python main.py
    set "APP_EXIT=!errorlevel!"
    goto :done
)
set "PYTHON_EXE="
for /d %%D in ("%LocalAppData%\Programs\Python\Python*" "%ProgramFiles%\Python*") do if not defined PYTHON_EXE if exist "%%~fD\python.exe" set "PYTHON_EXE=%%~fD\python.exe"
if defined PYTHON_EXE (
    "!PYTHON_EXE!" main.py
    set "APP_EXIT=!errorlevel!"
    goto :done
)
echo Python was not found. Install Python or add it to PATH.
set "APP_EXIT=1"
:done
pause
exit /b %APP_EXIT%