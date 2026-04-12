from playwright.sync_api import expect

from pages.base_page import base_page


class DashboardPage(base_page):

    MAIN_MENU_ITEMS = [
        "Admin",
        "PIM",
        "Leave",
        "Time",
        "Recruitment",
        "My Info",
        "Performance",
        "Dashboard",
        "Directory",
        "Maintenance",
        "Claim",
    ]

    SEARCH_INPUT = "input[placeholder='Search']"
    TEXT_WIDGETS = "//div [@class='orangehrm-dashboard-widget-name']/p"
    UPGRADE_BUTTON = "//button[contains(@class, 'orangehrm-upgrade-button')]"
    USER_DROPDOWN_TAB = "//span[contains(@class,'oxd-userdropdown-tab')]"
    HELP_ICON = "//i[contains(@class,'oxd-icon bi-question-lg')]"
    BRAND_LOGO = "//div[contains(@class,'oxd-brand-banner')]"
    PIM_MAIN_MENU_ITEM = "//a[@class='oxd-main-menu-item']/span[text()= 'PIM']"
    ADMIN_MAIN_MENU_ITEM = "//a[@class='oxd-main-menu-item']/span[text()= 'Admin']"
    MAIN_MENU_BUTTON = "//button[@class='oxd-icon-button oxd-main-menu-button']"
    USER_DROPDOWN = ".oxd-userdropdown-tab"
    USER_LOGOUT = "a[name='Logout']"

    MENU_ITEMS = ["About", "Support", "Change Password", "Logout"]

    def __init__(self, page):
        super().__init__(page)

        self.user_dropdown_tab_locator = self.page.locator(self.USER_DROPDOWN_TAB)
        self.search_textfield = self.page.locator(self.SEARCH_INPUT)
        self.pim_widget = self.page.locator(self.PIM_MAIN_MENU_ITEM)
        self.admin_widget = self.page.locator(self.ADMIN_MAIN_MENU_ITEM)
        self.main_menu_button = self.page.locator(self.MAIN_MENU_BUTTON)
        self.text_widgets = self.page.locator(self.TEXT_WIDGETS)

    def get_dashboard(self):
        return self.page.locator("//h6[text()='Dashboard']")

    def get_search_input(self):
        return self.search_textfield

    def search(self, text):
        self.search_textfield.fill(text)
        if not self.pim_widget.is_visible():
            return False
        return True

    def get_main_menu_items(self, name):
        return self.page.locator(
            f"//span[contains(@class,'oxd-main-menu-item--name') and normalize-space()='{name}']"
        )

    def get_text_of_widgets(self):
        return self.text_widgets.all_text_contents()

    def get_upgrade_button(self):
        return self.page.locator(self.UPGRADE_BUTTON)

    def get_help_icon(self):
        return self.page.locator(self.HELP_ICON)

    def get_brand_logo(self):
        return self.page.locator(self.BRAND_LOGO)

    def get_user_dropdown(self):
        return self.user_dropdown_tab_locator

    def click_user_dropdown(self):
        self.user_dropdown_tab_locator.click()

    def get_user_menu_items(self, name):
        return self.page.locator(
            f"//a[contains(@class,'oxd-userdropdown-link') and normalize-space()='{name}']"
        )

    def get_dropdown_menu_items_texts(self):
        return [
            text.strip()
            for text in self.page.locator(
                "//a[contains(@class,'oxd-userdropdown-link')]"
            ).all_text_contents()
        ]

    def click_main_menu_button(self):
        self.main_menu_button.click()

    def main_menu_pim_items_toggled(self):
        return self.page.locator(self.PIM_MAIN_MENU_ITEM)

    def logout(self):
        self.click_by_locator(self.USER_DROPDOWN)
        self.click_by_role("menuitem", name="Logout")
