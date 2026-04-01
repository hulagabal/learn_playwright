from pages.LoginPage import LoginPage


def test_login_page(page, logger):

    login_page = LoginPage(page)

    logger.info("Page opened")

    login_page.login()

    assert login_page.check_dashoboard() is False

    logger.info("Dashboard opened")
  
    
