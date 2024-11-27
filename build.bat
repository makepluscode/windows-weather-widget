@echo off
chcp 65001
echo [Building Weather Widget EXE]

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install pyinstaller if not installed
pip install pyinstaller

:: Create executable
pyinstaller --name WeatherWidget ^
            --onefile ^
            --windowed ^
            --icon=weather.ico ^
            --add-data ".env;." ^
            --hidden-import=dotenv ^
            main.py

:: Copy necessary files
copy .env dist\.env

echo.
echo Build complete! The executable is in the 'dist' folder.
echo.

pause