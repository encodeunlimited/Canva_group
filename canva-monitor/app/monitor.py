"""
Monitor module for Canva Monitor V2.
Evaluates the URL, extracts token, compares with database, and saves state.
"""
from app.utils import extract_canva_token
from app.database import get_current, save_current, add_history
from app.logger import logger

def check(url: str) -> bool:
    """
    Evaluates the newly captured URL.
    
    Args:
        url: The Canva invitation URL.
        
    Returns:
        True if the token is new and changed, False otherwise.
    """
    token = extract_canva_token(url)
    
    if not token:
        logger.error(f"Could not extract token from URL: {url}")
        return False
        
    logger.info(f"Current URL: {url}")
    logger.info(f"Token: {token}")
    
    previous = get_current()
    
    if not previous:
        # First run
        logger.info("First run detected. Saving to database.")
        save_current(url, token)
        add_history(url, token)
        return False
        
    prev_url, prev_token = previous
    
    if token != prev_token:
        # Changed
        logger.info("Change Detected!")
        save_current(url, token)
        add_history(url, token)
        return True
    else:
        # No change
        logger.info("No Change.")
        return False
