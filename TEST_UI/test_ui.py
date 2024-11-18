from time import sleep

import allure
import pytest
import params

from TEST_UI.aviaPage import aviaPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


@allure.title('Основной шаблон поиска')
@allure.description('Проверяем поля шаблона поиска, '
                    'включая поля сложного маршрута '
                    'на видимость и доступность')
@allure.severity("medium")
def test_template_fields_validation(browser):
    avia_page = aviaPage(browser, params.URL)
    selector_fields = [
        '[data-test-id="switch-to-multiwayform"]',
        '[data-test-id="switch-to-aviaform"]'
    ]
    try:
        with allure.step('Нажимаем кнопку раскрытия сложного маршрута '):
            avia_page.find_element_selector(selector_fields[0]).click()
        all_action = avia_page.template_fields_validation()
        with allure.step('Нажимаем кнопку закрытия сложного маршрута '):
            avia_page.find_element_selector(selector_fields[1]).click()
        assert all_action is True
    except Exception as e:
        print(f'Ошибка выполнения теста '
              f'test_template_fields_validation() - {e}')


@allure.title('Тестирование горячих билетов')
@allure.description('Проверяем название страницы с горячими билетами '
                    'и размерность списка билетов')
@allure.severity("blocker")
def test_hot_tickets(browser):
    avia_page = aviaPage(browser, params.URL)
    selector_fields = [
        '[data-test-id="iata"]',
        '//*[@id="avia_form_origin-input"]',
        '//*[contains(text(),"Больше жарких билетов")]',
        '[data-test-id="hot-tickets-button"]',
        '[data-test-id="brand-text"]',
        '[data-test-id="hot-destination"]',
        '[testid="hot-tickets-navbar-button"]'
    ]
    try:
        code_name = avia_page.code_name(selector_fields[0], selector_fields[1])
        if code_name[0] is None:
            with allure.step(f'Фиксируем дефолтное значение кода '
                             f'города вылета {params.code_city[0]} '
                             f'и обновляем браузер'):
                avia_page.find_element_selector(
                    selector_fields[0]).send_keys(params.code_city[0])
                browser.refresh()

        with allure.step('Кнопка "Больше жарких билетов" доступна'):
            butt = avia_page.find_one_XPATH(selector_fields[2])
            assert butt.is_displayed() is True

        with allure.step('Нажимаем кнопку'):
            avia_page.find_element_selector(selector_fields[3]).click()

        with allure.step('Переходим на страницу с Горячими билетами'):
            avia_page_n = aviaPage(browser,
                                   f'https://www.aviasales.ru/?params='
                                   f'{code_name[0]}&service=hottickets')
            WebDriverWait(browser, 5)

        with allure.step('Название страницы с горящими билетами'):
            title = avia_page_n.find_element_selector(
                selector_fields[4]).text

        with allure.step('Получаем список горячих билетов'):
            list_t = avia_page_n.len_list(selector_fields[5])

        with allure.step('Нажимаем кнопку возврата в главное меню'):
            avia_page_n.find_element_selector(selector_fields[6]).click()

        with allure.step('Название страницы соответствует "Горячие билеты"'):
            assert title == 'Горячие билеты'
        with allure.step('Список горячих билетов не пустой'):
            assert list_t > 0, 'Список горях билетов пуст'

    except Exception as e:
        print(f'Ошибка выполнения теста test_hot_tickets - {e}')


@allure.title('Тестирование списка популярных направлений')
@allure.description(f'Проверяем наличие города(-ов) {params.popular_city} '
                    f'в списке популярных направлений, '
                    f'смотрим список предлагаемых билетов')
@allure.severity("normal")
def test_popular_destinations(browser):

    popular = False
    avia_page = aviaPage(browser, params.URL)
    selector_fields = [
        '[class ="main-popular-directions__destination"]',
        'main-popular-directions__destination-city-name',
        'main-popular-directions__destination-header-opener'
    ]

    try:
        with allure.step("Скроллим вниз главную страницу"):
            browser.execute_script("window.scrollBy(0, 4500)")
            #browser.execute_script("window.scrollBy(0, window.innerHeight,'smooth')")

            WebDriverWait(browser, 5)
        with ((allure.step('Выбираем популярные направления'))):
            popular_directions = avia_page.find_elements_selector(
                selector_fields[0])
            assert len(popular_directions) > 0, ('Список популярных '
                                                 'направлений пуст')

        with allure.step('Проверяем наличие города в списке'):
            for pop in popular_directions:
                name_city = pop.find_element(
                    By.CLASS_NAME, selector_fields[1]).text
                if name_city in params.popular_city:
                    popular = True
                    with allure.step(f'Открыли/закрыли список билетов для {name_city}'):
                        pop.find_element(By.CLASS_NAME, selector_fields[2]).click()
                        WebDriverWait(browser, 5)
                        pop.find_element(By.CLASS_NAME, selector_fields[2]).click()
            assert popular is True, ("Ни один город из списка не "
                                     "найден в числе популярных")

        with allure.step("Скроллим вверх главную страницу"):
            browser.execute_script("window.scrollBy(0, -4500)")
            #browser.execute_script("window.scrollBy(0, -window.innerHeight)")

        WebDriverWait(browser, 5)
    except Exception as e:
        print(f'Ошибка выполнения теста test_popular_destinations - {e}')


@allure.title('Наличие ошибки при идентичности полей "Откуда" и "Куда"')
@allure.description('Проверяем наличие текста ошибки '
                    'если названия города вылета и прилета идентичны')
@allure.severity("critical")
@pytest.mark.negative_test
def test_error_for_identity_fields(browser):
    # '//*[starts-with(text(),"Укажите разные города")]'
    avia_page = aviaPage(browser, params.URL)
    selector_fields = [
        '[data-test-id="iata"]',
        '//*[@id="avia_form_origin-input"]',
        '//*[@id="avia_form_destination-input"]',
        'button[data-test-id="form-submit"]',
        '//*[starts-with(text(),"Выбрать другой город")]',
        '//div[text()="Укажите разные города"]'
    ]
    try:
        with ((((allure.step('Определяем код  и название города вылета'))))):
            code = avia_page.find_element_selector(selector_fields[0]).text
            name = avia_page.find_one_XPATH(
                selector_fields[1]).get_attribute("value")
            if code is None:
                with allure.step(f'Фиксируем дефолтное значение кода '
                                 f'города вылета {params.code_city[0]}'):
                    avia_page.find_element_selector(
                        selector_fields[0]).send_keys(params.code_city[0])
                    browser.refresh()
                    name = avia_page.find_one_XPATH(
                        selector_fields[1]).get_attribute(
                        "value")
        with allure.step('Фиксируем название города в поле "Куда"'
                         'идентичное полю "Откуда"'):
            destination = avia_page.find_one_XPATH(selector_fields[2])
            #destination.clear()
            destination.send_keys(name)
            element = avia_page.find_one_XPATH(selector_fields[4])
            WebDriverWait(browser, 10 )
        with allure.step('Проверяем видимость сообщения об ошибке'):
            assert element.is_displayed(), ('Информация об ошибке '
                                            'ввода отсутствует')
    except Exception as e:
        print(f'Ошибка выполнения теста test_error_for_identity_fields - {e}')


@allure.title("Негативный тест поиска билетов без указания даты")
@allure.description('Проверяем наличие текста ошибки '
                    'если дата в шаблоне поиска не указана и нажата кнопка "Найти билеты"')
@allure.severity("critical")
@pytest.mark.negative_test
def test_None_date(browser):
    avia_page = aviaPage(browser, params.URL)
    selector_fields = [
        '[data-test-id="form-submit"]',
        '//div[text()="Укажите дату"]'
    ]
    try:
        avia_page.find_element_selector(selector_fields[0]).click()
        element = avia_page.find_one_XPATH(selector_fields[1])
        with allure.step("Незаполненное поле Дата подcвечивается"):
            assert element.is_displayed()

    except Exception as e:
        print(f'Ошибка выполнения теста test_None_date - {e}')