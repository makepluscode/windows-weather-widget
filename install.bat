@echo off
chcp 65001
echo [Weather Widget Installation]
echo.

:: Python installation check
where python > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Save current directory path
set PROJECT_DIR=%CD%

:: Create virtual environment
echo Creating virtual environment...
if exist "%PROJECT_DIR%\venv" (
    echo Removing existing virtual environment...
    rmdir /s /q "%PROJECT_DIR%\venv"
)

:: Create venv
python -m venv venv

:: Verify venv creation
if not exist "%PROJECT_DIR%\venv\Scripts\activate.bat" (
    echo Failed to create virtual environment.
    echo Please check your Python installation.
    pause
    exit /b 1
)

:: Activate virtual environment and install packages
echo Installing required packages...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Install packages
python -m pip install --upgrade pip
pip install PySide6 requests python-dotenv

:: Create requirements.txt
pip freeze > requirements.txt

:: Create .env file if it doesn't exist
if not exist .env (
    echo WEATHER_API_KEY=your_api_key_here > .env
    echo .env file has been created. Please enter your API key.
)

echo.
echo Installation complete!
echo 1. Enter your API key in the .env file
echo 2. Run 'run.bat' to start the program
echo.

pause