
import pytest

from selenium import webdriver


@pytest.fixture(scope="class")
def init_driver(request):

    request.cls.driver = webdriver.Chrome()

    yield

    request.cls.driver.quit()