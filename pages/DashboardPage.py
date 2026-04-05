from unicodedata import name

from conftest import logger, page
from pages.BasePage import base_page
from playwright.sync_api import expect

class DashboardPage(base_page):

    MAIN_MENU_ITEMS = [
        "Admin", "PIM", "Leave", "Time", "Recruitment",
        "My Info", "Performance", "Dashboard", "Directory",
        "Maintenance", "Claim"]
    
    SEARCH_INPUT = "input[placeholder='Search']"
    TEST_WIDGETS = "//div [@class='orangehrm-dashboard-widget-name']/p"
    UPGRADE_BUTTON = "//button[contains(@class, 'orangehrm-upgrade-button')]"
    USER_DROPDOWN_TAB = "//span[contains(@class,'oxd-userdropdown-tab')]"
    HELP_ICON = "//i[contains(@class,'oxd-icon bi-question-lg')]"
    BRAND_LOGO = "//div[contains(@class,'oxd-brand-banner')]"
    PIM_MAIN_MENU_ITEM = "//a[@class='oxd-main-menu-item']/span[text()= 'PIM']"
    ADMIN_MAIN_MENU_ITEM = "//a[@class='oxd-main-menu-item']/span[text()= 'Admin']"
    MAIN_MENU_BUTTON = "//button[@class='oxd-icon-button oxd-main-menu-button']"

    def __init__(self, page):
        super().__init__(page)

        self.user_dropdown_tab_locator = self.page.locator(self.USER_DROPDOWN_TAB)
        self.search_textfield= self.page.locator(self.SEARCH_INPUT)
        self.pim_widget = self.page.locator(self.PIM_MAIN_MENU_ITEM)
        self.admin_widget = self.page.locator(self.ADMIN_MAIN_MENU_ITEM)
        self.main_menu_button = self.page.locator(self.MAIN_MENU_BUTTON)

    def search_textfield_visible(self):
        self.search_textfield.wait_for(state="visible", timeout=5000)
        return self.search_textfield.is_visible()
    
    def search(self, text):
        self.search_textfield.fill(text)
        self.pim_widget.wait_for(state="visible", timeout=5000)
        if not self.pim_widget.is_visible():
             return False
        return True

    MENU_ITEMS = [ "About", "Support", "Change Password", "Logout"]

    def get_main_menu_locator(self, name):
        return self.page.locator(
            f"//span[contains(@class,'oxd-main-menu-item--name') and normalize-space()='{name}']"
        )

    def main_menu_items_visible(self):
        for item in self.MAIN_MENU_ITEMS:
            self.get_main_menu_locator(item).wait_for(state="visible", timeout=5000)
            if not self.get_main_menu_locator(item).is_visible():
                 return False
        return True
    
    def get_text_of_widgets(self):
        return self.page.locator(self.TEST_WIDGETS).all_text_contents()
    
    def is_upgrade_button_visible(self):
        return self.page.locator(self.UPGRADE_BUTTON).is_visible()
    
    def help_icon(self):
        self.page.locator(self.HELP_ICON).wait_for(state="visible", timeout=5000)
        return self.page.locator(self.HELP_ICON).is_visible()
    
    def brand_logo_visible(self):
        return self.page.locator(self.BRAND_LOGO).is_visible()
        
    def is_user_dropdown_visible(self):
        self.user_dropdown_tab_locator.wait_for(state="visible", timeout=5000)  
        return self.user_dropdown_tab_locator.is_visible()

    def click_user_dropdown(self):
        self.user_dropdown_tab_locator.click()

    def get_user_menu_items(self, name):
        return self.page.locator(f"//a[contains(@class,'oxd-userdropdown-link') and normalize-space()='{name}']")
    
    def user_menu_items_visible(self):
        for item in self.MENU_ITEMS:
            self.get_user_menu_items(item).wait_for(state="visible", timeout=5000)
            if not self.get_user_menu_items(item).is_visible():
                return False
        return True

    def get_menu_items_texts(self):
        return [text.strip() for text in 
                self.page.locator("//a[contains(@class,'oxd-userdropdown-link')]").all_text_contents()]
    
    def click_main_menu_button(self):
        
        button=self.page.locator(self.MAIN_MENU_BUTTON)
        button.wait_for(state="visible", timeout=5000)
        button.click()
    
    def main_menu_items_toggled(self):
            
            pim=self.page.locator(self.PIM_MAIN_MENU_ITEM)
            pim.wait_for(state="hidden", timeout=5000)
            return pim.is_hidden()