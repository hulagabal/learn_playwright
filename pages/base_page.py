class base_page:

    def __init__(self, page):
        self.page = page

    def wait_for_url(self, url):
        self.page.wait_for_url(url)

    def open(self, url):
        self.page.goto(url)

    def fill_by_role(self, role, name, text):
        self.page.get_by_role(role, name=name).fill(text)

    def fill_by_placeholder(self, name, text):
        self.page.get_by_placeholder(name).fill(text)

    def get_Title(self):
        return self.page.title()

    def check_visible(self, locator):
        return self.page.locator(locator).is_visible()

    def click_by_locator(self, locator):
        element=self.page.locator(locator)
        element.wait_for(state="visible")
        element.wait_for(state="attached")
        element.click(timeout=10000)


    def fill_by_locator(self, locator, text):
        self.page.locator(locator).fill(text)

    def click_by_role(self, role, name):
        self.page.get_by_role(role, name=name).click()
