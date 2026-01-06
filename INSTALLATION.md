================================================================================
                    INSTALLATION GUIDE
          Stock Analyzer - USA Stock Analysis Tool
================================================================================

📋 SYSTEM REQUIREMENTS
================================================================================

Operating System:
  ✓ Windows 10/11
  ✓ macOS (Intel or Apple Silicon)
  ✓ Linux (Ubuntu 20.04+ recommended)

Python:
  ✓ Python 3.8 or higher
  ✓ pip (Python package manager)

Hardware:
  ✓ Minimum: 2GB RAM, 500MB free disk space
  ✓ Recommended: 4GB+ RAM, 1GB+ free disk space

Internet:
  ✓ Active internet connection (for API calls)
  ✓ Access to Yahoo Finance


🔧 INSTALLATION METHODS
================================================================================

METHOD 1: AUTOMATED SETUP (RECOMMENDED)
================================================================================

Windows Users:
  1. Open Command Prompt or PowerShell
  2. Navigate to project directory
  3. Run: setup.bat
  4. Wait for installation to complete
  5. Done! ✅

Linux/Mac Users:
  1. Open Terminal
  2. Navigate to project directory
  3. Run: bash setup.sh
  4. Wait for installation to complete
  5. Done! ✅


METHOD 2: MANUAL INSTALLATION
================================================================================

Step 1: Create Virtual Environment
  Windows:
    > python -m venv venv
    > venv\Scripts\activate

  Linux/Mac:
    $ python3 -m venv venv
    $ source venv/bin/activate

Step 2: Upgrade pip
  Windows:
    > python -m pip install --upgrade pip

  Linux/Mac:
    $ python3 -m pip install --upgrade pip

Step 3: Install Dependencies
  All platforms:
    $ pip install -r requirements.txt

Step 4: Verify Installation
  All platforms:
    $ python -c "import yfinance; print('✓ Installation successful')"


METHOD 3: CONDA INSTALLATION
================================================================================

If you use Anaconda:

  1. Create environment:
     conda create -n stock_analyzer python=3.10

  2. Activate environment:
     conda activate stock_analyzer

  3. Install dependencies:
     pip install -r requirements.txt

  4. Verify:
     python -c "import yfinance; print('✓ OK')"


⚙️ CONFIGURATION
================================================================================

1. Create Configuration File:
   Windows:
     > copy .env.example .env

   Linux/Mac:
     $ cp .env.example .env

2. Edit .env file with text editor:
   
   Optional configurations (leave blank to disable):
     - EMAIL_NOTIFICATIONS_ENABLED=True/False
     - SMTP_SERVER=your_smtp_server
     - SENDER_EMAIL=your_email@gmail.com
     - SENDER_PASSWORD=your_app_password
     - RECIPIENT_EMAIL=recipient@gmail.com
     - TELEGRAM_NOTIFICATIONS_ENABLED=True/False
     - TELEGRAM_BOT_TOKEN=your_bot_token
     - TELEGRAM_CHAT_ID=your_chat_id
     - WEBHOOK_URL=your_webhook_endpoint

3. Save the file


📦 DEPENDENCY INSTALLATION DETAILS
================================================================================

Core Dependencies:
  yfinance (0.2.32)
    → Downloads stock price data from Yahoo Finance
    → Install: pip install yfinance

  pandas (2.0.3)
    → Data manipulation and analysis
    → Install: pip install pandas

  numpy (1.24.3)
    → Numerical computing
    → Install: pip install numpy

Analysis Libraries:
  scikit-learn (1.3.0)
    → Machine learning library
    → Install: pip install scikit-learn

  ta (0.10.2)
    → Technical analysis indicators
    → Install: pip install ta

  tensorflow (2.13.0) - Optional
    → Deep learning (optional for advanced models)
    → Install: pip install tensorflow

Web/Dashboard:
  streamlit (1.25.0)
    → Web dashboard framework
    → Install: pip install streamlit

  plotly (5.14.0)
    → Interactive charts
    → Install: pip install plotly

Utilities:
  requests (2.31.0)
    → HTTP client
    → Install: pip install requests

  python-dotenv (1.0.0)
    → Environment variable management
    → Install: pip install python-dotenv


🐍 PYTHON VERSION COMPATIBILITY
================================================================================

Recommended: Python 3.10 or 3.11
Minimum: Python 3.8
Maximum Tested: Python 3.12

Check your Python version:
  Windows:
    > python --version

  Linux/Mac:
    $ python3 --version


✅ VERIFY INSTALLATION
================================================================================

Test 1: Check Python
  $ python --version
  Expected: Python 3.8 or higher

Test 2: Check pip
  $ pip --version
  Expected: pip version with Python path

Test 3: Check Virtual Environment
  Windows:
    > which python
  Linux/Mac:
    $ which python3
  Expected: Path to venv directory

Test 4: Check Key Packages
  $ python -c "import yfinance, pandas, numpy; print('✓ OK')"

Test 5: Test Data Fetching
  $ python cli.py analyze AAPL -p 1mo
  Expected: Stock analysis output

Test 6: Test Web Dashboard
  $ streamlit run dashboard.py
  Expected: Web browser opens at http://localhost:8501


🆘 TROUBLESHOOTING
================================================================================

Issue: "Python not found"
  Solution: 
    - Download Python from python.org
    - Add Python to PATH
    - Restart command prompt

Issue: "pip not found"
  Solution:
    - pip is installed with Python
    - Try: python -m pip --version
    - Update: python -m pip install --upgrade pip

Issue: "Module not found"
  Solution:
    - Ensure virtual environment is activated
    - Reinstall requirements: pip install -r requirements.txt

Issue: "yfinance connection error"
  Solution:
    - Check internet connection
    - Yahoo Finance servers may be down
    - Try again after a few minutes

Issue: "Port 8501 already in use"
  Solution (for Streamlit):
    - Kill the process using that port
    - Or use different port: streamlit run dashboard.py --server.port 8502

Issue: "Permission denied"
  Solution:
    - Linux/Mac: chmod +x setup.sh
    - Windows: Run as Administrator

Issue: "SSL Certificate Error"
  Solution:
    - pip install --upgrade certifi
    - Or set: PYTHONHTTPSVERIFY=0 (not recommended for production)


🔄 UPGRADING DEPENDENCIES
================================================================================

Update All Packages:
  $ pip install --upgrade -r requirements.txt

Update Specific Package:
  $ pip install --upgrade yfinance

Check for Updates:
  $ pip list --outdated


🚀 QUICK TEST
================================================================================

After installation, verify everything works:

1. Command Line Test:
   $ python cli.py analyze AAPL

   Expected output:
     ============================================================
     STOCK ANALYSIS REPORT: AAPL
     ============================================================
     📊 TECHNICAL INDICATORS:
       Current Price: $XXX.XX
       ...

2. Dashboard Test:
   $ streamlit run dashboard.py

   Expected result:
     - Web browser opens
     - Dashboard loads with stock selector
     - Can select stocks and view analysis

3. Python API Test:
   $ python
   >>> from main import StockAnalyzerApp
   >>> app = StockAnalyzerApp()
   >>> result = app.analyze_single_stock('AAPL')
   >>> print(result['technical']['latest_price'])
   XXX.XX
   >>> exit()


📂 FILE STRUCTURE AFTER INSTALLATION
================================================================================

stock_analyzer/
├── venv/                    # Virtual environment (after setup)
├── logs/                    # Log files (created on first run)
│
├── main.py
├── cli.py
├── dashboard.py
├── requirements.txt
├── .env                     # Your configuration
│
├── config/
│   └── settings.py
│
├── src/
│   ├── data/
│   ├── analysis/
│   ├── signals/
│   ├── notifications/
│   └── ai/
│
└── tests/
    └── test_analyzer.py


🔐 SECURITY SETUP
================================================================================

1. Secure .env File:
   Windows:
     - Right-click .env
     - Properties → Security
     - Remove read access for other users

   Linux/Mac:
     $ chmod 600 .env

2. API Keys:
   - Generate new API keys if sharing code
   - Don't commit .env to version control
   - Use environment variables in production

3. Firewall:
   - Streamlit dashboard (default port 8501)
   - Only allow trusted connections


🎓 POST-INSTALLATION
================================================================================

After successful installation:

1. Read Documentation:
   - START_HERE.txt
   - README.md
   - QUICK_START.txt

2. First Analysis:
   $ python cli.py analyze AAPL MSFT GOOGL -p 6mo

3. Explore Dashboard:
   $ streamlit run dashboard.py

4. Try All Features:
   - Buy signals: python cli.py buy AAPL MSFT
   - Sell signals: python cli.py sell AAPL MSFT
   - Hot stocks: python cli.py hot AAPL MSFT GOOGL

5. Customize Settings:
   - Edit config/settings.py
   - Update .env for notifications


🆘 GET HELP
================================================================================

Check Documentation:
  - README.md (comprehensive guide)
  - ARCHITECTURE.md (system design)
  - USAGE.md (advanced usage)
  - QUICK_START.txt (quick reference)

View Logs:
  Windows:
    > type logs\stock_analyzer.log

  Linux/Mac:
    $ tail -f logs/stock_analyzer.log

Run Tests:
  $ python -m pytest tests/

Check Code Comments:
  - Each module has detailed docstrings
  - Functions have examples
  - See usage patterns in code


📝 NEXT STEPS
================================================================================

1. Installation: ✅ DONE
2. Configuration: Read .env.example
3. First Run: python cli.py analyze AAPL
4. Explore: Try all commands
5. Customize: Adjust settings for your needs
6. Learn: Read documentation
7. Integrate: Use Python API in your code


================================================================================
                    Installation Complete! 🎉
            You're ready to analyze USA stocks! 📈
================================================================================

Next: Read START_HERE.txt or run:
  $ python cli.py analyze AAPL MSFT GOOGL -p 1y

Or launch dashboard:
  $ streamlit run dashboard.py

Good luck! 🚀
