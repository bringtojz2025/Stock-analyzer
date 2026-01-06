#!/bin/bash

# Setup script for Stock Analyzer

echo "🚀 Setting up Stock Analyzer..."
echo ""

# Create virtual environment
echo "1️⃣  Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "2️⃣  Activating virtual environment..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install requirements
echo "3️⃣  Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
echo "4️⃣  Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env created. Please update with your settings."
else
    echo "⚠️  .env already exists."
fi

# Create logs directory
echo "5️⃣  Creating logs directory..."
mkdir -p logs

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "  1. Update .env with your API keys and notification settings"
echo "  2. Run: python main.py"
echo "  3. Or: python cli.py analyze AAPL MSFT GOOGL"
echo "  4. Or: streamlit run dashboard.py"
