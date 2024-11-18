import allure
import pytest


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@allure.step('Открытие и закрытие браузера')
@pytest.fixture(scope="session")
def browser():
    """
    Основная фикстура по инициализации браузера
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--headless")
    with allure.step('Открытие браузера'):
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        driver.implicitly_wait(4)
    yield driver

    with allure.step('Закрытие браузера'):
        driver.quit()
