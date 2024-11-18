import allure
import pytest

from TEST_API.apiPage import apiPage


@allure.title("Список билетов по заданному маршруту в оба направления")
@allure.description('Проверяем получение списка билетов с '
                    'валидными первичными данными полета')
@allure.severity("critical")
@pytest.mark.positive_test
@pytest.mark.parametrize('code_city, data, base_url, res',
                          [(["MOW", "STW"],
                            ["2024-12-15", "2024-12-09"],
                            "https://min-prices.aviasales.ru/price_matrix?",
                            0)
                          ])
def test_get_tow_way(code_city, data, base_url, res):
    with allure.step('Первичные данные для поиска определены '
                     'в параметрах теста'):
        apitest=apiPage(base_url)
    with allure.step('Выполняем запрос'):
        response =apitest.get_json(
            #f'{apitest.base_url}' +
            f'origin_iata={code_city[0]}&destination_iata={code_city[1]}&'
            f'depart_start={data[0]}& return_start ={data[1]}&'
            f'depart_range=6&return_range=6&affiliate=false&market=ru')
    with (allure.step('Количество элементов в списке '
                     'полученных билетов >0 ')):
        assert  len(response["prices"]) > res, ('Список '
        'билетов по заданному маршуруту не найден')


@allure.title("Запрос на получение списка горячих билетов")
@allure.description(f'Проверяем что список горячих билетов не пустой и '
                    f'есть билеты заданной авиакомпании')
@allure.severity("medium")
@pytest.mark.positive_test
@pytest.mark.parametrize('code_city, code_air, base_url, status, res',
                          [('LED','S7',
                            'https://ariadne.aviasales.com/api/gql',
                            200, True
                            )
                          ])
def test_hot_tickets(code_city, code_air, base_url, status, res):
    apitest = apiPage(base_url)
    with allure.step('Фиксируем первичные данные для поиска '):
        params= {
            "operation_name": "hot_offers",
            "query": '\nquery HotOffersV1(\n $input: HotOffersV1Input!, \n $brand: Brand!, \n '
                     '$locales: [String!]\n ) {\n  hot_offers_v1(input: $input, brand: $brand) {\n '
                     'offers {\n price {\n ...priceWithDestinationCityIataFields\n }\n '
                     'old_price {\n  value\n } \n  }\n cities {\n  ...citiesFields\n  }\n '
                     'airlines {\n  ...airlinesFields\n  }\n airports {\n ...airportsFields\n '
                     '}\n countries {\n ...countriesFields\n }\n }\n  '
                     '}\n\nfragment priceWithDestinationCityIataFields on Price {\n '
                     '...priceFields\n  destination_city_iata\n}\n\nfragment priceFields on Price '
                     '{\n  depart_date\n  return_date\n  value\n  cashback\n  found_at\n '
                     'signature\n  ticket_link\n  currency\n  provider\n  with_baggage\n '
                     'segments {\n  transfers {\n   duration_seconds\n country_code\n '
                     'visa_required\n   night_transfer\n  at\n  to\n  tags\n  }\n '
                     'flight_legs {\n  origin\n destination\n  local_depart_date\n '
                     'local_depart_time\n   local_arrival_date\n  local_arrival_time\n '
                     'flight_number\n  operating_carrier\n  aircraft_code\n  technical_stops\n '
                     'equipment_type\n duration_seconds\n }\n }\n}\n\n\nfragment airlinesFields '
                     'on Airline {\n iata\n translations(filters: {locales: $locales})\n}\n\n'
                     'fragment citiesFields on CityInfo {\n city {\n  iata\n '
                     'translations(filters: {locales: $locales})\n '
                     '}\n}\n\nfragment airportsFields on Airport {\n '
                     'iata\n  translations(filters: {locales: $locales})\n '
                     'city {\n  iata\n translations(filters: {locales: $locales})\n '
                     '}\n}\n\nfragment countriesFields on Country {\n  iata\n '
                     'translations(filters: {locales: $locales})\n}\n',
            "variables": {
                "brand": "AS",
                "locales": [
                    "ru"
                ],
                "input":
                    {
                        "origin_iata": f"{code_city}",
                        "origin_type": "CITY",
                        "currency": "rub",
                        "market": "ru",
                        "one_way": True,
                        "trip_class": "Y",
                        "max_directions": 50,
                        "group_by": "NONE"
                    }
            }
        }
    with allure.step('Выполняем запрос'):
        response = apitest.post_obj(json = params)
    with allure.step('Получаем JSON ответа'):
        lst=response.json()
    with allure.step(f'Проверяем наличии в списке авиакомпании {code_air}'):
        test_air = False
        for air in lst["data"]["hot_offers_v1"]["airlines"]:
            if air["iata"] == code_air:
                test_air = True
    with allure.step(f'Статус исполнения запроса = {status}'):
        assert response.status_code == status
    with allure.step('Json ответа  не пустой'):
        assert lst is not None
    with allure.step(f'В списке присутсвуют билеты авиакомпании c кодом {code_air}'):
        assert test_air is res


@allure.title("Запрос на получение информации о городе, установленному по дефолту")
@allure.description('Проверяем соответствие названия города вылета установенному значению')
@allure.severity("medium")
@pytest.mark.positive_test
@pytest.mark.parametrize('code_city, base_url, status',
              [('Барнаул',
                'https://suggest.aviasales.com/v2/nearest_places.json?locale=ru_RU',
                200 )
              ])
def test_city_default(code_city, base_url, status):
    with allure.step(f'Задаем город для проверки соответствия c '
                     f'дефолтным значением {code_city}'):
       apitest = apiPage(base_url)
    with allure.step('Выполняем запрос'):
        response = apitest.get_obj("")
    with allure.step('Получаем JSON ответа'):
        res =  response.json()
    with allure.step('Статус исполнения запроса = 200'):
        assert response.status_code == status
    with allure.step(f'Проверка соответствия города по дефолту заданному -  {code_city}'):
        assert res[0]["name"] == code_city, ('Город по умолчанию не сооответствует заданному')


@allure.title("Запрос на получение авиарейсов с  идентичными городами вылета и прилета")
@allure.description('Проверяем наличие ошибки при исполнении запроса с невалидными данными по выбранным городам')
@allure.severity("critical")
@pytest.mark.negative_test
@pytest.mark.parametrize('code_city, data, base_url, status',
              [(["MOW", "MOW"],["2024-12-15", "2024-12-09"],
                'https://min-prices.aviasales.ru/price_matrix?',
                200)
              ])
def test_search_parameters_negative(code_city,data, base_url, status):
    with allure.step(f'Фиксируем первичные невалидные данные для поиска по кодам городов маршрута : {code_city}'):
        apitest=apiPage(base_url)
        #code_city = ["MOW", "MOW"]
        #data = ["2024-12-15", "2024-12-09"]
        #BASE_URL = "https://min-prices.aviasales.ru/price_matrix?"
    with allure.step('Выполняем запрос'):
        #response = requests.get(
        #f'{BASE_URL}' +
        response = apitest.get_obj(f'origin_iata={code_city[0]}&'
                                   f'destination_iata={code_city[1]}&'
                                   f'depart_start={data[0]}&'
                                   f'return_start ={data[1]}&depart_range=6&'
                                   f'return_range=6&'
                                   f'affiliate=false&market=ru')
    with allure.step('Получаем JSON ответа'):
        lst = response.json()
    with allure.step('Статус исполнения запроса = 200'):
        assert response.status_code==status
    with allure.step(f'В ответе присутствует информация об '
                     f'ошибке в теле запроса : {lst["errors"]}'):
        assert lst["errors"] is not None


@allure.title('Запрос на получение информации со страницы "Короче"')
@allure.description('Проверяем наличие быстрых фильтров на странице "Короче" ')
@allure.severity("normal")
@pytest.mark.positive_test
@pytest.mark.parametrize('page_title, base_url, status',
              [('Короче о городах',
                'https://trap.aviasales.ru/api/v2/guides?locale=ru_RU&brand=AS',
                200)
              ])
def test_page_info(page_title, base_url, status):
    with allure.step('Фиксируем URL для запроса'):
        apitest=apiPage(base_url)
    with allure.step('Выполняем запрос'):
        response = apitest.get_obj("")
    with allure.step('Получаем JSON ответа'):
        lst = response.json()
    with allure.step('Выбираем в ответе фильтры'):
        filters = lst["search_filters"]
    with allure.step(f'Статус исполнения запроса = {status}'):
        assert response.status_code==status
    with allure.step(f'Название страницы соответвтует заявленной - {page_title}'):
        assert lst["header"]["title"] == page_title
    with allure.step('Количество фильтров на странице > 0'):
        assert len(filters)>0
