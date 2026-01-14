from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import time


def parser_site(*, url, driver: WebDriver) -> list[str]:
    """
    Парсинг главной страницы сайт и сбор номеров заказов. 

    :return: Description
    :rtype: list[str, str, str...]
    """
    items_id = []
    
    # Переходим на нужную страницу и ждем прогрузку + 5 секунд для загрущки JS.
    driver.get(f"{url}&page=1")
    time.sleep(5)

    # Ниже полный цикл копирования номеров заказа и отправка их в список .
    while True:
        time.sleep(1)
        items_elements = driver.find_elements(By.CLASS_NAME, "m-sidebar__layout--found-item")
        if items_elements:
            for item in items_elements:
                item_id = item.find_element(By.CLASS_NAME, "m-found-item__num")
                id_str = (item_id.text)[2:]
                items_id.append(id_str)
        
        # FIXME: На данный момент переход на следующие выполнен очень плохо и топорно, бывает падает и ловить баги... 
        # НО работает для v0.1.
        next_li = driver.find_element(
            By.XPATH,
            '//li[contains(@class,"page-item") and .//a[@aria-label="Next"]]'
        )

        # Нужен только для выхода со страницы.
        if "disabled" in next_li.get_attribute("class"): # type: ignore
            break
        
        next_li.find_element(By.TAG_NAME, "a").click()

    return items_id


def parser_local_site(*, site, items, driver: WebDriver) -> list[str]:
    """
    Парсим страницы заказов вызванные из функции parser_site и из списка items

    :return: Description
    :rtype: list[[str,str,str...], [str,str,str...]...]
    """

    list_items = [] # Нужен только для сбора данных
    for item in items:
        # TODO: Создаем ссылку на сайт, переходим по этой ссылке...
        # Перезагружаем страницу так как объекты сканирования накладываються...
        # Ждем 2 секунды на refresh и отправляеться марсить страницу.
        new_site = f"{site}/#/ext(popup:item/{item}/advert)"
        driver.get(new_site)
        driver.refresh()
        time.sleep(2)

        # FIXME: Сбор данных, можно изменить только переменные в будущем.
        item_id = (driver.find_element(By.CLASS_NAME, "m-modal__num").text)[2:]
        name_product = driver.find_element(By.CLASS_NAME, "m-modal__title.m-title.m-title--h2.ng-star-inserted").text
        owner_product = (driver.find_element(By.CLASS_NAME, "m-infoblock__layout.ng-star-inserted").text)[9:]
        price_product = (driver.find_elements(By.CLASS_NAME, "m-infoblock__layout.ng-star-inserted")[1].text)[18:]
        
        GlobalStart_date = driver.find_element(By.CLASS_NAME, "m-rangebox__layout")
        start_date = GlobalStart_date.find_element(By.CLASS_NAME, "m-rangebox__date.ng-star-inserted").text
        GlobalEnd_date = driver.find_element(By.CLASS_NAME, "m-rangebox__layout.m-rangebox__layout--rtl")
        end_date = GlobalEnd_date.find_element(By.CLASS_NAME, "m-rangebox__date.ng-star-inserted").text

        # Создаем удобный для нас массив и отправляет его в глобальный массив данных.
        item = [new_site, item_id, start_date, end_date, name_product, owner_product, price_product]
        list_items.append(item)
    return list_items


def main_parser(*, site, url) -> list[str]:
    #FIXME: Подключаем драйвер и сразу запускаем бразуер. Долго
    driver = webdriver.Edge()

    # Сперва собираем данные номеров заказа...
    # Проходимся по номерам локально и собираем данные там.
    items_list = parser_site(url=url, driver=driver)
    items_data = parser_local_site(site=site, items=items_list, driver=driver)
    
    # Завершаем driver - закрываем браузер...
    # Смотрим данные и отправляем их назад.
    driver.quit()
    if items_data:
        return items_data
    return []

