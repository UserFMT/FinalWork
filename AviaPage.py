import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class AviaPage:

    def __init__(self, driver: webdriver.Chrome, URL: str) -> None:
        self._driver = driver
        self._driver.get(URL)
        self._driver.maximize_window()
        self._driver.implicitly_wait(5)

    @allure.step('Поиск одного элемента по CSS_SELECTOR')
    def find_elements_selector(self, selector: str) -> list[WebElement]:
        return self._driver.find_elements(By.CSS_SELECTOR, selector)

    @allure.step('Поиск списка элементов по CSS_SELECTOR')
    def find_element_selector(self, selector: str) -> WebElement:
        return self._driver.find_element(By.CSS_SELECTOR, selector)

    @allure.step('Поиск одного элемента по CSS_SELECTOR')
    def find_one_XPATH(self, selector: str) -> WebElement:
        return self._driver.find_element(By.XPATH, selector)
