"""
Configuration module for Canva Monitor V2.
Loads configuration from environment variables or uses default values.
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Configuration Variables
BINGO_URL = os.getenv("BINGO_URL", "https://bingotingo.com/best-social-media-platforms/")
WAIT_SECONDS = int(os.getenv("WAIT_SECONDS", "30"))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))  # 30 seconds

BOT_TOKEN = os.getenv("BOT_TOKEN", "8606686386:AAHSD0OaxC9FjyI79kD2eQaUyF12wsPg1n4")
CHAT_ID = os.getenv("CHAT_ID", "8274409214")

HEADLESS = os.getenv("HEADLESS", "true").lower() in ("true", "1", "t", "yes", "y")

DATABASE_PATH = str(DATA_DIR / "monitor.db")
LOG_PATH = str(LOGS_DIR / "monitor.log")
