from playwright.sync_api import TimeoutError
import time


# 🔥 SAFE CLICK
def safe_click(page, locator, *, timeout=15000, retries=2, wait_for=None, logger=None):
    for attempt in range(retries + 1):
        try:
            if logger:
                logger.info(f"[CLICK] Attempt {attempt+1}")

            locator.wait_for(state="visible", timeout=timeout)
            locator.scroll_into_view_if_needed()

            locator.click(timeout=timeout)

            # Post action wait
            if wait_for:
                if isinstance(wait_for, str):
                    page.wait_for_url(wait_for, timeout=timeout)
                else:
                    wait_for.wait_for(state="visible", timeout=timeout)

            return True

        except TimeoutError as e:
            if logger:
                logger.warning(f"[CLICK FAILED] Attempt {attempt+1}: {e}")

            if attempt == retries:
                raise

            time.sleep(1)


# ✍️ SAFE TYPE
def safe_type(locator, text, *, timeout=15000, clear=True, logger=None):
    if logger:
        logger.info(f"[TYPE] Entering text: {text}")

    locator.wait_for(state="visible", timeout=timeout)

    if clear:
        locator.fill("")  # clear field

    locator.fill(text, timeout=timeout)


# 👁️ SAFE GET TEXT
def safe_get_text(locator, *, timeout=15000, logger=None):
    locator.wait_for(state="visible", timeout=timeout)

    text = locator.inner_text()

    if logger:
        logger.info(f"[TEXT] Got text: {text}")

    return text


# ⏳ WAIT FOR ELEMENT
def wait_for_element(locator, *, timeout=15000, state="visible", logger=None):
    if logger:
        logger.info(f"[WAIT] Waiting for element state: {state}")

    locator.wait_for(state=state, timeout=timeout)


# 🌐 WAIT FOR URL
def wait_for_url(page, url_pattern, *, timeout=15000, logger=None):
    if logger:
        logger.info(f"[WAIT] Waiting for URL: {url_pattern}")

    page.wait_for_url(url_pattern, timeout=timeout)


# 🔍 IS VISIBLE (SAFE CHECK)
def is_visible(locator, *, timeout=5000):
    try:
        locator.wait_for(state="visible", timeout=timeout)
        return True
    except TimeoutError:
        return False


# 📸 SCREENSHOT (Reusable)
def take_screenshot(page, name="screenshot"):
    import os
    from datetime import datetime

    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{folder}/{name}_{timestamp}.png"

    page.screenshot(path=path)
    return path