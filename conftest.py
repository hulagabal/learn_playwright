import pytest
from playwright.sync_api import sync_playwright
import os
import logging
import datetime


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:   
        browser = p.chromium.launch(headless=False,slow_mo=1000) 
        
        yield browser
        # browser.close()


def pytest_addoption(parser):
    parser.addini("base_url", "Base URL for tests")

@pytest.fixture(scope="function")
def page(browser, request):
    base_url=request.config.getini("base_url")
    context = browser.new_context()
    page = context.new_page()
    page.goto(base_url)
    yield page
    page.close()

@pytest.fixture(scope="session")
def logger():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler("logs/test.log")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)
        if page:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=f"screenshots/failure_{timestamp}.png")