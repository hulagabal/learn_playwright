import re

import pytest
from playwright.sync_api import expect

from pages.dashboard_page import DashboardPage

EXPECTED_WIDGET_TEXTS = [
    "Time at Work",
    "My Actions",
    "Quick Launch",
    "Employees on Leave Today",
    "Employee Distribution by Sub Unit",
    "Employee Distribution by Location",
]
EXPECTED_MENU_ITEM_TEXTS = ["About", "Support", "Change Password", "Logout"]


@pytest.mark.smoke
@pytest.mark.dashboard
@pytest.mark.ui
@pytest.mark.regression
def test_dashboard_header_and_user_dropdown(authenticated_user, page):


    expect(authenticated_user.get_brand_logo()).to_be_visible()
    expect(authenticated_user.get_help_icon()).to_be_visible()
    expect(authenticated_user.get_upgrade_button()).to_be_visible()
    expect(authenticated_user.get_search_input()).to_be_visible()
    

    expect(authenticated_user.get_user_dropdown()).to_be_visible()
    authenticated_user.click_user_dropdown()

    for item in authenticated_user.MENU_ITEMS:
        expect(authenticated_user.get_user_menu_items(item)).to_be_visible()

    

    actual_dropdown_menu_item_texts = authenticated_user.get_dropdown_menu_items_texts()
    print(actual_dropdown_menu_item_texts)
    assert actual_dropdown_menu_item_texts == EXPECTED_MENU_ITEM_TEXTS
    

@pytest.mark.dashboard
@pytest.mark.regression
def test_main_menu_button_and_search(authenticated_user, page):

    expect(authenticated_user.get_main_menu_items("Admin")).to_be_visible()
    expect(authenticated_user.get_main_menu_items("PIM")).to_be_visible()
    

    authenticated_user.click_main_menu_button()

    for item in authenticated_user.MAIN_MENU_ITEMS:
        expect(authenticated_user.get_main_menu_items(item)).to_be_hidden()
    

    authenticated_user.click_main_menu_button()

    for item in authenticated_user.MAIN_MENU_ITEMS:
        expect(authenticated_user.get_main_menu_items(item)).to_be_visible()
    

    authenticated_user.search("PIM")
    expect(authenticated_user.pim_widget).to_be_visible()
    expect(authenticated_user.admin_widget).to_be_hidden()
    


@pytest.mark.dashboard
@pytest.mark.regression
def test_dashboard_widgets(authenticated_user, page):

    actual_widget_texts = set(authenticated_user.get_text_of_widgets())
    EXPECTED_WIDGET_TEXTS_SET = set(EXPECTED_WIDGET_TEXTS)
    assert EXPECTED_WIDGET_TEXTS_SET.issubset(actual_widget_texts)
    
