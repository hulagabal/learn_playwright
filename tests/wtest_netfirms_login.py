
from playwright.sync_api import expect
from pages.NetfirmsLoginPage import Netfirms_Login_page

def test_valid_Login(page):
    netfirms_login_page = Netfirms_Login_page(page)
    netfirms_login_page.login("autotestcieig42324", "Muttu!134111111111111111111")

    expect(page).to_have_url("**/controlpanel/**")


    
    assert page.locator("[data-qe-id='nav-main-domains']").is_visible()
    assert page.locator("[data-qe-id='nav-main-hosting']").is_visible()
    assert page.locator("[data-qe-id='nav-main-business']").is_visible()
    