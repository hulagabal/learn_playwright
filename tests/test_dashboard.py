import re

import pytest
from pages.DashboardPage import DashboardPage
from playwright.sync_api import expect


EXPECTED_WIDGET_TEXTS = ['Time at Work', 'My Actions', 'Quick Launch', 'Buzz Latest Posts',
                              'Employees on Leave Today', 'Employee Distribution by Sub Unit',
                                'Employee Distribution by Location']
EXPECTED_MENU_ITEM_TEXTS = ["About", "Support", "Change Password", "Logout"]

@pytest.mark.smoke
@pytest.mark.dashboard
@pytest.mark.ui
def test_dashboard_header_and_main_menu(authenticated_user, page, logger):

    dashboard_page = DashboardPage(page)
    
    expect(page).to_have_url(re.compile(r"/dashboard/index$"))
    expect(authenticated_user.get_dashboard()).to_be_visible()
    logger.info("Orange HRM dashboard is visible after login.")

    expect(dashboard_page.brand_logo()).to_be_visible()
    expect(dashboard_page.help_icon()).to_be_visible()
    expect(dashboard_page.upgrade_button()).to_be_visible()
    expect(dashboard_page.search_textfield).to_be_visible()
    logger.info("Dashboard header elements are visible.")
    

    dashboard_page.search("PIM")
    expect(dashboard_page.pim_widget).to_be_visible(timeout=5000)
    expect(dashboard_page.admin_widget).to_be_hidden(timeout=5000)
    dashboard_page.search_textfield.clear()
    logger.info("Search works as expected.")

    for item in dashboard_page.MAIN_MENU_ITEMS:
        expect(dashboard_page.get_main_menu_locator(item)).to_be_visible(timeout=5000)
    logger.info("All menu items are visible on the dashboard.")

@pytest.mark.dashboard
def test_main_menu_button_and_menu_items(authenticated_user, page, logger):    
    dashboard_page = DashboardPage(page)

    expect(authenticated_user.get_dashboard()).to_be_visible()

    expect(dashboard_page.get_main_menu_locator("Admin")).to_be_visible(timeout=5000)

    dashboard_page.click_main_menu_button()

    for item in dashboard_page.MAIN_MENU_ITEMS:
        expect(dashboard_page.get_main_menu_locator(item)).to_be_hidden(timeout=5000)
    logger.info("Main menu items hidden successfully.")

    dashboard_page.click_main_menu_button()

    for item in dashboard_page.MAIN_MENU_ITEMS:
        expect(dashboard_page.get_main_menu_locator(item)).to_be_visible()   
    
    logger.info("Menu expanded successfully.")

@pytest.mark.dashboard
def test_dashboard_widgets_and_user_dropdown(authenticated_user, page, logger):
    dashboard_page = DashboardPage(page)

    expect(authenticated_user.get_dashboard()).to_be_visible()

    widget_texts = dashboard_page.get_text_of_widgets()

    assert sorted(widget_texts) == sorted(EXPECTED_WIDGET_TEXTS)
    logger.info("All dashboard widgets are displayed with correct titles.")

    expect(dashboard_page.user_dropdown()).to_be_visible()
    dashboard_page.click_user_dropdown()

    for item in dashboard_page.MENU_ITEMS:
        expect(dashboard_page.get_user_menu_items(item)).to_be_visible(timeout=5000)
    
    logger.info("All user dropdown menu items are visible.")

    actual_dropdown_menu_item_texts = dashboard_page.get_dropdown_menu_items_texts()

    assert actual_dropdown_menu_item_texts == EXPECTED_MENU_ITEM_TEXTS
    logger.info("All user dropdown menu items have correct titles.")