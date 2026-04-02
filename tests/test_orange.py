
import pytest
from pages.OrangePage import Orange_Page
import pytest_check as check

@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.login
@pytest.mark.ui
def test_valid_login(authenticated_user,page, logger):

    assert page.url.endswith("/dashboard/index")
    assert authenticated_user.is_dashboard_visible()

    # check.is_true("dashboard" in page.url.lower())
    # check.is_true(orangePage.is_dashboard_visible())
    
    logger.info("Valid Login test passed")

@pytest.mark.regression
def test_invalid_login(page,logger):

    orange=Orange_Page(page)
    orange.login("Admin","Admin")

    assert page.url.endswith("/login")
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
def test_login_logout(authenticated_user,page,logger):
   
   authenticated_user.logout()

   assert page.url.endswith("/login")
   assert authenticated_user.is_login_button_visible()

   logger.info("Login Logout Test Passed")

@pytest.mark.regression
def test_session_persistence(authenticated_user, page, logger):

    page.reload()
    page.wait_for_timeout(3000)

    assert page.url.endswith("/dashboard/index")  
    assert authenticated_user.is_dashboard_visible()

    logger.info("Test Session persistence test passed")