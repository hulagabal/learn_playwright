import pytest
from playwright.sync_api import sync_playwright
import os
import logging
import datetime
from pages.OrangePage import Orange_Page
from utils.utils import get_datestamp

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:   
        browser = p.chromium.launch(headless=False,slow_mo=1000) 
        
        yield browser
        browser.close()


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

@pytest.fixture(scope="function")
def authenticated_user(page, logger):
    logger.info("Starting login fixture")
    orange=Orange_Page(page)
    username = os.getenv("ORANGE_USERNAME", "Admin")
    password = os.getenv("ORANGE_PASSWORD", "admin123")
    orange.login(username, password)
    yield orange
    logger.info("Endend login fixture")

@pytest.fixture(scope="session")
def logger():

    time_stamp = get_datestamp()
    folder_path=os.path.join("reports", "logs")
    if os.path.exists(folder_path) and not os.path.isdir(folder_path):
        os.remove(folder_path)
    os.makedirs(folder_path, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_path = os.path.join(folder_path, f"test_{time_stamp}.log")
    file_handler = logging.FileHandler(file_path)
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
            folder_path=os.path.join("reports", "screenshots")
            os.makedirs(folder_path, exist_ok=True)
            test_name = item.name
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{test_name}_{report.when}_{timestamp}.png"
            full_path = os.path.join(folder_path, file_name)
            page.screenshot(path=full_path)