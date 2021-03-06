from behave import fixture, use_fixture
from selenium.webdriver import Chrome


@fixture
def browser_chrome(context):
    context.browser = Chrome()
    context.browser.maximize_window()
    yield context.browser
    context.browser.quit()


def before_all(context):
    use_fixture(browser_chrome, context)