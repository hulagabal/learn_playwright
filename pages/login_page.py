from pages.base_page import base_page


class Orange_Page(base_page):
    USERNAME = 'input[name="username"]'
    PASSWORD = 'input[name="password"]'
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = "p.oxd-alert-content-text"
    REQUIRED_ERROR = "text=Required"

    def __init__(self, page):
        super().__init__(page)

    def enter_username(self, username):
        self.page.locator(self.USERNAME).fill(username)

    def enter_password(self, password):
        self.page.locator(self.PASSWORD).fill(password)

    def click_login(self):
        self.page.locator(self.LOGIN_BUTTON).click()
        self.page.wait_for_timeout(3000)

    def login(self, username, password):
        self.fill_by_locator(self.USERNAME, username)
        self.fill_by_locator(self.PASSWORD, password)
        self.click_by_locator(self.LOGIN_BUTTON)
        self.page.wait_for_timeout(3000)

    def get_error_message_text(self):
        return self.page.locator(self.ERROR_MESSAGE).text_content()

    def get_error_message(self):
        return self.page.locator(self.ERROR_MESSAGE)

    def required_error_count(self):
        return self.page.locator(self.REQUIRED_ERROR).count()

    def get_required_error_message(self):
        self.page.wait_for_timeout(1000)
        return self.page.locator(self.REQUIRED_ERROR).first

    def get_login_button(self):
        return self.page.locator(self.LOGIN_BUTTON)
