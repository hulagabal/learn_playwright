
import pytest
from pages.OrangePage import Orange_Page
import pytest_check as check

@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.login
@pytest.mark.ui
def test_valid_login(logged_in_page,page, logger):

    page.wait_for_timeout(3000)

    assert page.url.endswith("/dashboard/index")

    assert logged_in_page.is_dashboard_visible()

    # check.is_true("dashboard" in page.url.lower())
    # check.is_true(orangePage.is_dashboard_visible())
    
    logger.info("Valid Login test passed")

@pytest.mark.regression
def test_invalid_login(page,logger):

    orange=Orange_Page(page)

    orange.login("Admin","Admin")

    assert "login" in page.url.lower()

    assert orange.is_error_visible()

    assert "Invalid credentials" in orange.get_error_message()

    logger.info("Invalid Login test passed")

@pytest.mark.regression
def test_empty_login(page, logger):

    orange=Orange_Page(page)

    orange.click_login()        
    
    assert page.url.endswith("login")

    assert orange.is_required_error_visible()
    
    assert orange.required_error_count() >= 1

    logger.info("Empty Login test passed")

@pytest.mark.regression
def test_login_logout(page,logger):
    
    orange=Orange_Page(page)
    orange.login("Admin", "admin123")

    orange.logout()

    assert page.url.endswith("/login")

    logger.info("Login Logout Test Passed")

@pytest.mark.regression
def test_session_persistence(logged_in_page, page, logger):

    page.reload()
    page.wait_for_timeout(3000)

    assert page.url.endswith("/dashboard/index")  
    assert logged_in_page.is_dashboard_visible()

    logger.info("Test Session persistence test passed")