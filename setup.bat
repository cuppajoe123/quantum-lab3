@echo off

if exist .venv (
    echo Virtual environment already exists. Removing and creating a new one...
    rmdir /s /q .venv
)

echo Creating Python virtual environment...
python -m venv .venv

if not exist .venv (
    echo Error: Failed to create virtual environment.
    echo Please ensure Python is installed and in your PATH.
    goto :end
)

echo Activating virtual environment...
.venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install .

if errorlevel 1 (
    echo Error: Failed to install dependencies.
    echo Please check the error messages above.
) else (
    echo ================================================
    echo Setup complete! Please run the following command to activate your environment:
    echo .venv\Scripts\activate.bat
    echo ================================================
)

:end
echo.
pause
