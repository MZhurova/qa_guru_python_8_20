import pytest
from selene import browser


@pytest.fixture
def api_url():
    return 'https://demowebshop.tricentis.com/'


@pytest.fixture(scope='function')
def setup_browser(request):
    browser.config.base_url = "https://demowebshop.tricentis.com"
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield browser

    browser.quit()
