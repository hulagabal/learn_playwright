from pages.BasePage import base_page

class Orange_Page(base_page):
    USERNAME= 'input[name="username"]'
    PASSWORD= 'input[name="password"]'
    LOGIN_BUTTON= "button[type='submit']"
    ERROR_MESSAGE = "p.oxd-alert-content-text"
    REQUIRED_ERROR = "text=Required"
    USER_DROPDOWN = ".oxd-userdropdown-tab"
    USER_LOGOUT = "a[name='Logout']"

    def __init__(self, page):
        super().__init__(page)

    def enter_username(self, username):
        self.page.locator(self.USERNAME).fill(username)

    def enter_password(self, password):
        self.page.locator(self.PASSWORD).fill(password)

    def click_login(self):
        self.page.locator(self.LOGIN_BUTTON).click()
        self.page.wait_for_timeout(3000)

    def is_dashboard_visible(self):
        locator = self.page.locator("//h6[text()='Dashboard']")
        locator.wait_for(state="visible", timeout=5000)
        return locator.is_visible()
    
    def login(self, username, password):
        self.fill_by_locator(self.USERNAME, username)
        self.fill_by_locator(self.PASSWORD, password)
        self.click_by_locator(self.LOGIN_BUTTON)
        self.page.wait_for_timeout(3000)


    def get_error_message(self):
        return self.page.locator(self.ERROR_MESSAGE).text_content()

    def is_error_visible(self):
        error_message=self.page.locator(self.ERROR_MESSAGE)
        error_message.wait_for(state="visible")
        return error_message.is_visible()
    

    def required_error_count(self):
        return self.page.locator(self.REQUIRED_ERROR).count()
    

    def is_required_error_visible(self):
        self.page.wait_for_timeout(1000)
        return self.page.locator(self.REQUIRED_ERROR).first.is_visible()

    def logout(self):
        self.click_by_locator(self.USER_DROPDOWN)    
        self.click_by_role("menuitem", name="Logout")
        
    def is_login_button_visible(self):
        return self.page.locator(self.LOGIN_BUTTON).is_visible()    