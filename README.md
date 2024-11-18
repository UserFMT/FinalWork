# Дипломное задание
  UI и API  тестирование  сайта 'https://www.aviasales.ru/'
  Тестирование без этапа авторизации пользователем.
  Документация сайта отсутствует в открытом доступе, тестирование API осуществлялось 
  по запросам панели разработчика (F12).

### Окружение
  - pytest~=8.3.3
  - selenium==4.26.1
  - allure-pytest~=2.13.5
  - requests ~=2.32.3


### Используемые библиотеки
  - pyp install pytest
  - pip install selenium
  - pip install webdriver-manager
  - pip install requests
  - pip install allure-pytest

### Струткура:
- папка TEST_UI :
   - описание методов для основной страницы сайта - AviaPage.py
   - набор тестов - test_api.py
     Для тестирования использован браузер Google Chrome 
- папка TES_API :
   - описание методов для основной страницы сайта - apiPage.py
   - параметры для тестов UI - params.py
   - набор тестов - test_ui.py
-   определение тестов необходимы к запуску - pytest.ini
-   объявление используемых фикстур - conftest.py

## Шаги
1. Склонировать проект 'https://github.com/UserFMT/FinalWork.git'
2. Установить зависимости
3. Запустить тесты 
     pytest --alluredir allure-result   или  python -m pytest --alluredir allure-result
4. Сформировать отчет  
     allure serve allure-result

## Полезные ссылки

