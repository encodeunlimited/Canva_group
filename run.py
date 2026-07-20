#!/usr/bin/env python3
"""
Main entry point for Canva Monitor V2.
Orchestrates the monitoring loop, error handling, and notifications.
"""
import time
from datetime import datetime

from config.config import CHECK_INTERVAL
from app.logger import logger
from app.browser import get_canva_url
from app.monitor import check
from app.notifier import send
from app.utils import extract_canva_token

def main() -> None:
    """Main loop for the Canva Monitor."""
    logger.info("Starting Canva Monitor V2...")
    first_check = True
    
    while True:
        try:
            logger.info("-" * 40)
            logger.info("Initiating check cycle...")
            
            url = get_canva_url()
            changed = check(url)
            
            if changed or first_check:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                token = extract_canva_token(url)
                
                header = "🚨 <b>Canva Group Updated</b>" if changed else "🟢 <b>Monitor Started - Current Link</b>"
                
                message = (
                    f"{header}\n\n"
                    "<b>Invite Link</b>\n"
                    f"{url}\n\n"
                    "<b>Token</b>\n"
                    f"<code>{token}</code>\n\n"
                    "<b>Time</b>\n"
                    f"{timestamp}"
                )
                if send(message):
                    logger.info("Telegram Sent")
                    
                first_check = False
            
        except Exception as e:
            logger.error(f"Error during check cycle: {e}. Retrying on next interval.")
            logger.info("Retry scheduled.")
            
        logger.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Monitor stopped by user.")
