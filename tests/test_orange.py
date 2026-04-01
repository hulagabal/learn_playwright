
from pages.OrangePage import Orange_Page
import pytest_check as check


def test_valid_login(page, logger):
    
    orange=Orange_Page(page)

    orange.login("Admin", "admin123")
    
    page.wait_for_timeout(3000)

    assert page.url.endswith("/dashboard/index")

    assert orange.is_dashboard_visible()

    # check.is_true("dashboard" in page.url.lower())
    # check.is_true(orangePage.is_dashboard_visible())
    
    logger.info("Valid Login test passed")


def test_invalid_login(page,logger):

    orange=Orange_Page(page)

    orange.login("Admin","Admin")

    assert "login" in page.url.lower()

    assert orange.is_error_visible()

    assert "Invalid credentials" in orange.get_error_message()

    logger.info("Invalid Login test passed")

def test_empty_login(page, logger):

    orange=Orange_Page(page)

    orange.click_login()        
    
    assert page.url.endswith("login")

    assert orange.is_required_error_visible()
    
    assert orange.required_error_count() >= 1

    logger.info("Empty Login test passed")

def test_login_logout(page,logger):
    
    orange=Orange_Page(page)
    orange.login("Admin", "admin123")

    orange.logout()

    assert page.url.endswith("/login")
    logger.info("Login Logout Test Passed")

def test_session_persistence(page, logger):
    orange=Orange_Page(page)
    orange.login("Admin", "admin123")

    page.reload()

    assert page.url.endswith("/dashboard/index")  
    page.wait_for_timeout(3000)

    assert orange.is_dashboard_visible()

    logger.info("Test Session persistence test passed")