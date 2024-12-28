@echo off
echo Setting up the environment...

REM Create virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

echo Setup complete! You can now run the app.
pause
