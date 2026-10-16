@echo off
chcp 65001 >nul
cd /d "%~dp0\.."
setlocal EnableExtensions EnableDelayedExpansion
where py >nul 2>nul
if not errorlevel 1 (
    py -3 api\server.py
    goto :done
)
where python >nul 2>nul
if not errorlevel 1 (
    python api\server.py
    goto :done
)
set "PYTHON_EXE="
for /d %%D in ("%LocalAppData%\Programs\Python\Python*" "%ProgramFiles%\Python*") do if not defined PYTHON_EXE if exist "%%~fD\python.exe" set "PYTHON_EXE=%%~fD\python.exe"
if defined PYTHON_EXE (
    "!PYTHON_EXE!" api\server.py
    goto :done
)
echo Python was not found. Install Python or add it to PATH.
:done
pause