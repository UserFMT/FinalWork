import allure
import params

from AviaPage import AviaPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


browser = webdriver.Chrome()
avia_page = AviaPage(browser, params.URL)


@allure.title('Наличие предустановленного значения в поле "Откуда"')
def test_1():
    try:
        origin = avia_page.find_one_XPATH(
            '//*[@id="avia_form_origin-input"]')
        assert origin.get_attribute("value") is not None
    except Exception as e:
        print(f'Ошибка выполнения теста 1 - {e}')


@allure.title('Все поля шаблона поиска видимы и доступны для ввода')
def test_2():
    try:
        all_action = True
        origin = avia_page.find_elements_selector('[tabindex="0"]')
        for org in origin:
            if not (org.is_displayed()) and not (org.is_enabled()):
                all_action = False
        assert all_action
    except Exception as e:
        print(f'Ошибка выполнения теста  2 - {e}')


@allure.title('Получение списка горячих билетов из города вылета')
def test_3():
    try:
        with (allure.step('Определяем код города вылета '
                          'для перехода по новому URL')):
            code_sity = avia_page.find_element_selector(
                '[data-test-id="iata"]').text

        with (allure.step('Проверяем доступность кнопки '
                          '"Больше жарких билетов"')):
            butt = avia_page.find_one_XPATH(
                '//*[contains(text(),"Больше жарких билетов")]')
            assert butt.is_displayed() is True
            butt = avia_page.find_element_selector(
                '[data-test-id="hot-tickets-button"]')
            butt.click()

        with allure.step('Переходим на страницу с Горячими билетами и '
                         'проверяем что их количество больше 0'):
            avia_page_n = AviaPage(browser,
                                   f'https://www.aviasales.ru/?params='
                                   f'{code_sity}&service=hottickets')
            assert avia_page_n.find_element_selector(
                '[data-test-id="brand-text"]').text == 'Горячие билеты'
            list_t = avia_page_n.find_elements_selector(
                '[data-test-id="hot-tickets-lists-all-destinations"]')
            browser.close()
            assert len(list_t) > 0

    except Exception as e:
        print(f'Ошибка выполнения теста 3 - {e}')


@allure.title(f'Наличие в списке популярных направлений  города '
              f'{params.popular_city}')
def test_4():
    try:
        popular = False
        popular_directions = avia_page.find_elements_selector(
            '[class ="main-popular-directions__destination-city-name"]')
        assert len(popular_directions) > 0, \
            'Список популярных направлений пуст'
        for pop in popular_directions:
            if pop.text == params.popular_city:
                popular = True
                return
        assert popular

    except Exception as e:
        print(f'Ошибка выполнения теста 4 - {e}')


@allure.title('Проверка идентичности полей  "Откуда" и "Куда"')
def test_5():
    try:
        with allure.step('В поле ввода "Куда" '
                         'фиксируем значение идентичное полю "Откуда"'):
            destination = avia_page.find_one_XPATH(
                '//*[@id="avia_form_destination-input"]')
            destination.clear()
            destination.send_keys(avia_page.find_one_XPATH(
                '//*[@id="avia_form_origin-input"]').
                                  get_attribute("value"))
        with allure.step('Нажатие кнопки "Найти билеты"'):
            avia_page.find_element_selector(
                '[data-test-id="form-submit"]'
            ).click()
        with allure.step('Ожидаем появление текста ошибки'):
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//*[contains(text(),"Укажите разные города")]')))
        assert element.is_displayed()
    except Exception as e:
        print(f'Ошибка выполнения теста  5 - {e}')


browser.quit()
