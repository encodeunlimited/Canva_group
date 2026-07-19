"""
Notifier module for Canva Monitor V2.
Handles sending messages via Telegram Bot API.
"""
import requests
import time

from config.config import BOT_TOKEN, CHAT_ID
from app.logger import logger

def send(message: str, max_retries: int = 3) -> bool:
    """
    Sends a message to the configured Telegram chat.
    Retries on network failure. Never crashes the application.
    
    Args:
        message: The text message to send.
        max_retries: Maximum number of retry attempts.
        
    Returns:
        True if successful, False otherwise.
    """
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        logger.warning("Telegram Bot Token is not configured. Skipping notification.")
        return False
        
    if not CHAT_ID or CHAT_ID == "YOUR_TELEGRAM_CHAT_ID":
        logger.warning("Telegram Chat ID is not configured. Skipping notification.")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Telegram send failed (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                time.sleep(5)
                
    logger.error("Failed to send Telegram notification after all retries.")
    return False
