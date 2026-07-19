"""
Browser module for Canva Monitor V2.
Uses Playwright to automate the interaction and capture the final Canva URL.
"""
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Response
from typing import Optional

from config.config import BINGO_URL, WAIT_SECONDS, HEADLESS
from app.logger import logger

def get_canva_url() -> str:
    """
    Opens BingoTingo, waits for the countdown, clicks download, handles the 
    Biozium redirect and form submission, and captures the final Canva URL.
    
    Returns:
        The final redirected Canva URL as a string.
        Raises exceptions on failure for the calling loop to handle retries.
    """
    logger.info("Browser Start")
    final_url = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # 1. Open BingoTingo URL
            logger.info(f"Navigating to {BINGO_URL}")
            page.goto(BINGO_URL, timeout=60000, wait_until="domcontentloaded")
            
            # 2. Wait 65 seconds (plus a little buffer)
            logger.info(f"Waiting {WAIT_SECONDS} seconds for countdown...")
            page.wait_for_timeout((WAIT_SECONDS + 5) * 1000)
            
            # 3. Click Download
            download_link = page.locator("a#download, a.download-btn, a[href*='biozium']").first
            if download_link.count() > 0:
                logger.info("Download link found. Clicking...")
                with context.expect_page() as new_page_info:
                    download_link.click()
                new_page = new_page_info.value
                new_page.wait_for_load_state("domcontentloaded")
                target_page = new_page
            else:
                logger.warning("Could not find standard download button. Will try looking for #getForm on current page.")
                target_page = page

            # 4. Wait for Biozium / Submit #getForm
            logger.info("Waiting for #getForm...")
            target_page.wait_for_selector("#getForm", timeout=30000)
            logger.info("Submitting #getForm...")
            
            # 5. Capture final Canva URL via response interception or navigation
            def handle_response(response: Response):
                nonlocal final_url
                if response.status in (301, 302, 303, 307, 308):
                    location = response.headers.get("location", "")
                    if "canva.com/brand/join" in location:
                        final_url = location
            
            target_page.on("response", handle_response)
            
            with context.expect_page(timeout=30000) as final_page_info:
                target_page.locator("#getForm button").click(force=True)

            final_page = final_page_info.value
            final_page.wait_for_load_state("domcontentloaded")
            
            logger.info(f"Final URL: {final_page.url}")
            
            if "canva.com" in final_page.url:
                final_url = final_page.url
            else:
                raise Exception(f"Unexpected final URL: {final_page.url}")
                
        except PlaywrightTimeoutError as e:
            logger.error(f"Browser Timeout: {e}")
            raise
        except Exception as e:
            logger.error(f"Browser Error: {e}")
            raise
        finally:
            logger.info("Browser End. Closing context and browser.")
            context.close()
            browser.close()

    return final_url
