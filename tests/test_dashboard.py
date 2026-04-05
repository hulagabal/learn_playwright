from time import sleep

import pytest
from pages.DashboardPage import DashboardPage
from playwright.sync_api import expect


expected_widget_texts = ['Time at Work', 'My Actions', 'Quick Launch', 'Buzz Latest Posts',
                              'Employees on Leave Today', 'Employee Distribution by Sub Unit', 'Employee Distribution by Location']
expected_menu_item_texts = ["About", "Support", "Change Password", "Logout"]

@pytest.mark.smoke
@pytest.mark.dashboard
@pytest.mark.ui
def test_dashboard_header_and_main_menu(authenticated_user, page, logger):

    dashboard_page = DashboardPage(page)
    
    assert page.url.endswith("/dashboard/index")
    assert authenticated_user.is_dashboard_visible()
    logger.info("Orange HRM dashboard is visible after login.")

    assert dashboard_page.brand_logo_visible(), "Brand logo is not visible on the dashboard."
    logger.info("Brand logo is visible on the dashboard.")

    assert dashboard_page.help_icon(), "Help icon is not visible on the dashboard."
    logger.info("Help icon is visible on the dashboard.")

    assert dashboard_page.is_upgrade_button_visible(), "Upgrade button is not visible on the dashboard."
    logger.info("Upgrade button is visible on the dashboard.")

    assert dashboard_page.search_textfield_visible(), "Search text field is not visible on the dashboard."
    logger.info("Search text field is visible on the dashboard.")

    dashboard_page.search("PIM")
    logger.info("PIM widget is visible after searching for 'PIM'.")

    assert not dashboard_page.admin_widget.is_visible() , "Admin widget should not be visible after searching for 'PIM'."
    logger.info("Admin widget is not visible after searching for 'PIM'.")

    dashboard_page.search_textfield.clear()

    assert dashboard_page.main_menu_items_visible(), "Not all main menu items are visible."
    logger.info("All menu items are visible on the dashboard.")

@pytest.mark.dashboard
def test_main_menu_button_and_menu_items(authenticated_user, page, logger):    
    dashboard_page = DashboardPage(page)

    assert page.url.endswith("/dashboard/index")
    assert authenticated_user.is_dashboard_visible()
    logger.info("Orange HRM dashboard is visible after login.")

    expect(dashboard_page.get_main_menu_locator("Admin")).to_be_visible(timeout=5000)

    dashboard_page.click_main_menu_button()
    logger.info("Main menu button clicked.")

    assert dashboard_page.main_menu_items_toggled(), "Main menu items did not toggle correctly."
    logger.info("Main menu items hidden successfully.")

    dashboard_page.click_main_menu_button()

    assert dashboard_page.main_menu_items_visible(), "Main menu items are not visible after clicking the main menu button again."
    logger.info("Menu expanded successfully.")

@pytest.mark.dashboard
def test_dashboard_widgets_and_user_dropdown(authenticated_user, page, logger):
    dashboard_page = DashboardPage(page)

    assert authenticated_user.is_dashboard_visible()

    widget_texts = dashboard_page.get_text_of_widgets()

    assert widget_texts == expected_widget_texts, f"Expected widget texts: {expected_widget_texts}, but got: {widget_texts}"
    logger.info("All dashboard widgets are displayed with correct titles.")

    assert dashboard_page.is_user_dropdown_visible(), "User dropdown is not visible on the dashboard."
    logger.info("User dropdown is visible on the dashboard.")

    dashboard_page.click_user_dropdown()

    assert dashboard_page.user_menu_items_visible(), "Not all user dropdown menu items are visible."
    logger.info("All user dropdown menu items are visible.")

    actual_menu_item_texts = dashboard_page.get_menu_items_texts()

    assert actual_menu_item_texts == expected_menu_item_texts, f"Expected user dropdown menu items: {expected_menu_item_texts}, but got: {actual_menu_item_texts}"
    logger.info("All user dropdown menu items have correct titles.")