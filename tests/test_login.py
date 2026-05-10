import re

import pytest
import pytest_check as check
from playwright.sync_api import expect

from pages.login_page import Orange_Page
from utils.data_loader import get_user


@pytest.mark.critical
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.login
def test_valid_login(authenticated_user, page):

    expect(page).to_have_url(re.compile(r"/dashboard/index$"))
    expect(authenticated_user.get_dashboard()).to_be_visible()

    # check.is_true("dashboard" in page.url.lower())


@pytest.mark.regression
@pytest.mark.login
def test_invalid_login(page):

    user = get_user("invalid_user")
    orange = Orange_Page(page)
    orange.login(user["username"], user["password"])

    expect(orange.get_error_message()).to_be_visible()
    expect(orange.get_error_message()).to_contain_text("Invalid credentials")


@pytest.mark.regression
@pytest.mark.login
def test_empty_login(page):

    orange = Orange_Page(page)
    orange.click_login()

    expect(page).to_have_url(re.compile(r"/login$"))
    expect(orange.get_required_error_message()).to_be_visible()
    expect(orange.get_required_error_message()).to_have_text("Required")


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.regression
def test_login_logout(authenticated_user, page):

    authenticated_user.logout()
    expect(page).to_have_url(re.compile(r"/login$"))
    orange = Orange_Page(page)
    expect(orange.get_login_button()).to_be_visible()
    

@pytest.mark.regression
@pytest.mark.login
def test_session_persistence(authenticated_user, page):

    expect(page).to_have_url(re.compile(r"/dashboard/index$"))
    

    page.reload()
    page.wait_for_timeout(3000)

    expect(page).to_have_url(re.compile(r"/dashboard/index$"))
    expect(authenticated_user.get_dashboard()).to_be_visible()
    
