@echo off
REM Setup script for Stock Analyzer on Windows

echo.
echo 🚀 Setting up Stock Analyzer...
echo.

REM Create virtual environment
echo 1️⃣  Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 2️⃣  Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 3️⃣  Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file
echo 4️⃣  Creating .env file...
if not exist .env (
    copy .env.example .env
    echo ✅ .env created. Please update with your settings.
) else (
    echo ⚠️  .env already exists.
)

REM Create logs directory
echo 5️⃣  Creating logs directory...
if not exist logs mkdir logs

echo.
echo ✅ Setup complete!
echo.
echo 📖 Next steps:
echo   1. Update .env with your API keys and notification settings
echo   2. Run: python main.py
echo   3. Or: python cli.py analyze AAPL MSFT GOOGL
echo   4. Or: streamlit run dashboard.py
echo.
pause
