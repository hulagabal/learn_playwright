import re
import pytest
from pages.OrangeLoginPage import Orange_Page
import pytest_check as check
from playwright.sync_api import expect

@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.login
@pytest.mark.ui
def test_valid_login(authenticated_user,page, logger):

    expect(page).to_have_url(re.compile(r"/dashboard/index$"))
    expect(authenticated_user.get_dashboard()).to_be_visible()

    # check.is_true("dashboard" in page.url.lower())
    
    logger.info("Valid Login test passed")

@pytest.mark.regression
def test_invalid_login(page,logger):

    orange=Orange_Page(page)
    orange.login("Admin","Admin")

    expect(orange.get_error_message()).to_be_visible()
    expect(orange.get_error_message()).to_contain_text("Invalid credentials")

    logger.info("Invalid Login test passed")

@pytest.mark.regression
def test_empty_login(page, logger):

    orange=Orange_Page(page)
    orange.click_login()        
    
    expect(page).to_have_url(re.compile(r"/login$"))
    expect(orange.get_required_error_message()).to_be_visible()
    expect(orange.get_required_error_message()).to_have_text("Required")
    logger.info("Empty Login test passed")

@pytest.mark.regression
def test_login_logout(authenticated_user,page,logger):
   
   authenticated_user.logout()
   expect(page).to_have_url(re.compile(r"/login$"))
   orange=Orange_Page(page)
   expect(orange.get_login_button()).to_be_visible()
   logger.info("Login Logout Test Passed")

@pytest.mark.regression
def test_session_persistence(authenticated_user, page, logger):

    expect(page).to_have_url(re.compile(r"/dashboard/index$"))
    logger.info("Dashboard loaded after login")

    page.reload()
    page.wait_for_timeout(3000)

    expect(page).to_have_url(re.compile(r"/dashboard/index$"))
    expect(authenticated_user.get_dashboard()).to_be_visible()
    logger.info("Test Session persistence test passed")