chcp 65001
@echo off
echo [Starting Weather Widget]

:: Save current directory path
set PROJECT_DIR=%CD%

:: Activate virtual environment
call "%PROJECT_DIR%\venv\Scripts\activate.bat"

:: Run program
python3 main.py

:: Deactivate virtual environment
call "%PROJECT_DIR%\venv\Scripts\deactivate.bat"

pause