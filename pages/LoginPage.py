from pages.OrangePage import Orange_Page


def test_login(page):
    orange = Orange_Page(page)

    orange.enter_username("Admin")
    orange.enter_password("admin123")
    orange.click_login()

    page.wait_for_url("**/dashboard")

    assert orange.is_dashboard_visible()