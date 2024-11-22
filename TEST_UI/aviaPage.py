import allure


from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class aviaPage:

    def __init__(self, driver, URL: str) -> None:
        self._driver = driver
        self._driver.get(URL)

    @allure.step('Поиск списка элементов по селектору')
    def find_elements_selector(self, selector: str) -> list[WebElement]:
        return self._driver.find_elements(By.CSS_SELECTOR, selector)

    @allure.step('Поиск одного элемента по селектору')
    def find_element_selector(self, selector: str) -> WebElement:
        return self._driver.find_element(By.CSS_SELECTOR, selector)

    @allure.step('Поиск одного элемента по его месторасположению')
    def find_one_XPATH(self, selector: str) -> WebElement:
        return self._driver.find_element(By.XPATH, selector)

    @allure.step('Видимость и доступность полей ввода шаблона')
    def template_fields_validation(self) -> bool:
        selector_fields = [
            '[aria-autocomplete="list"]',
            '[data-test-id="passengers-field"]',
            '[data-test-id="multiway-date"]'
        ]
        all_action = True
        origin = (self.find_elements_selector(selector_fields[0]) +
                  self.find_elements_selector(selector_fields[2]))
        origin.extend(self.find_elements_selector(selector_fields[1]))
        for org in origin:
            with allure.step(f'{org.tag_name} - '
                             f'доступность {org.is_displayed()} - '
                             f'видимость {org.is_enabled()}'):
                if not (org.is_displayed()) and not (org.is_enabled()):
                    all_action = False
        return all_action

    @allure.title('Атрибуты города вылета ')
    def code_name(self, selector1, selector2: str) -> list[str]:
        with allure.step('Определяем код  и название города вылета'):
            code = self.find_element_selector(selector1).text
            name = self.find_one_XPATH(selector2).get_attribute("value")
        return [code, name]

    @allure.title('Размерность полученного списка')
    def len_list(self, selector: str) -> int:
        list = self.find_elements_selector(selector)
        return len(list)
