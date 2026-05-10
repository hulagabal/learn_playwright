import os
from datetime import datetime

import pytest
from playwright.sync_api import expect, sync_playwright

from logger import get_logger
from pages.dashboard_page import DashboardPage
from pages.login_page import Orange_Page
from report import HtmlReport
from utils.data_loader import get_user

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.firefox.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


def pytest_addoption(parser):
    parser.addini("BASE_URL", "Base URL for tests")


@pytest.fixture(scope="function")
def page(context, request):
    base_url = request.config.getini("BASE_URL")
    page = context.new_page()
    page.goto(base_url)
    yield page
    page.close()


@pytest.fixture(scope="function")
def authenticated_user(page, request):
    
    orange = Orange_Page(page)

    user = get_user("valid_user")
    username = user["username"]
    password = user["password"]

    orange.login(username, password)
    dashboard_page = DashboardPage(page)
    expect(dashboard_page.get_dashboard()).to_be_visible()
    yield dashboard_page
    
# global objects
html_report = None
logger = get_logger()

SCREENSHOT_DIR = "reports/screenshots"
REPORT_DIR = "reports"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


# 🚀 SESSION START
def pytest_sessionstart(session):
    global html_report
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(REPORT_DIR, f"report_{timestamp}.html")
    html_report = HtmlReport(report_path)

    logger.info("=== Test Session Started ===")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    # Screenshots must attach here; pytest-rerunfailures sets outcome to "rerun" later.
    if rep.when != "call" or not rep.failed:
        return
    funcargs = getattr(item, "funcargs", None) or {}
    page = funcargs.get("page")
    if not page:
        return
    filename = f"{item.name}.png"
    abs_path = os.path.join(SCREENSHOT_DIR, filename)
    rel_path = f"screenshots/{filename}"
    page.screenshot(path=abs_path)
    setattr(rep, "_custom_screenshot_rel", rel_path)


def pytest_runtest_logreport(report):
    global html_report
    if html_report is None:
        return

    when = report.when
    oc = getattr(report, "outcome", None)

    if when == "call":
        pass
    elif when == "setup" and oc == "skipped":
        pass
    elif when == "setup" and oc == "failed":
        pass
    elif when == "teardown" and oc == "failed":
        pass
    else:
        return

    test_name = report.nodeid
    duration = getattr(report, "duration", 0) or 0

    if oc == "rerun":
        status = "RERUN"
        message = (
            str(report.longrepr).strip()
            if report.longrepr
            else "Failed — scheduled for retry"
        )
    elif oc == "passed":
        status = "PASSED"
        message = "Test executed successfully"
    elif oc == "failed":
        if when == "setup":
            status = "SETUP ERROR"
        elif when == "teardown":
            status = "TEARDOWN ERROR"
        else:
            status = "FAILED"
        message = (
            report.longreprtext.strip()
            if getattr(report, "longreprtext", None)
            else (str(report.longrepr) if report.longrepr else "Test failed")
        )
    elif oc == "skipped":
        status = "SKIPPED"
        message = (
            report.longreprtext.strip()
            if getattr(report, "longreprtext", None)
            else "Test skipped"
        )
    else:
        return

    screenshot_path = getattr(report, "_custom_screenshot_rel", None)

    html_report.add_result(test_name, duration, status, message, screenshot_path)
    logger.info(f"{test_name} - {status}")
    if oc == "failed":
        logger.error(message)


# 🏁 SESSION FINISH
def pytest_sessionfinish(session, exitstatus):
    if html_report is not None:
        html_report.generate()
    logger.info("=== Test Session Finished ===")