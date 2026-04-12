from playwright.sync_api import expect

from pages.netfirms_login_page import Netfirms_Login_page


def test_valid_Login(page):
    netfirms_login_page = Netfirms_Login_page(page)
    netfirms_login_page.login("autotestcieig42324", "Muttu!134111111111111111111")

    expect(page).to_have_url("**/controlpanel/**")

    expect(page.locator("[data-qe-id='nav-main-domains']")).to_be_visible()
    expect(page.locator("[data-qe-id='nav-main-hosting']")).to_be_visible()
    expect(page.locator("[data-qe-id='nav-main-business']")).to_be_visible()
