#!/bin/bash
# Install script for Canva Monitor V2

echo "Starting Canva Monitor V2 Installation..."

# Update and install system dependencies if needed
sudo apt update
sudo apt install -y python3-venv python3-pip sqlite3

# Create virtual environment
echo "Creating Virtual Environment..."
python3 -m venv venv

# Activate venv and install python requirements
echo "Installing Python Dependencies..."
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt

# Install Playwright browsers (Chromium only)
echo "Installing Playwright Browsers..."
playwright install chromium
playwright install-deps chromium

# Create necessary directories
echo "Creating directories..."
mkdir -p data logs screenshots
chmod -R 755 data logs screenshots

echo "Installation Complete!"
echo "Please configure config/config.py and run 'python run.py' to start."
