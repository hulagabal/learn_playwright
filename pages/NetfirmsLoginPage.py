
from pages.BasePage import base_page

class Netfirms_Login_page(base_page):
    
    def __init__(self, page):
        super().__init__(page)

    def login(self, username, password):
        self.page.locator('input[name="credential_0"]').fill(username)
        self.page.locator('input[name="credential_1"]').fill(password)
        self.page.locator('#controlPanelLogin').click()
        self.page.wait_for_timeout(1000)