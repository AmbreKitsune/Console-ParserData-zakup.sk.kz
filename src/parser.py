from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

import save_data

def parser_site(*, url, driver: WebDriver) -> list[str]:
    """
    Парсинг главной страницы сайт и сбор номеров заказов. 

    :return: Description
    :rtype: list[str, str, str...]
    """
    items_id = []
    new_list_id = []
    old_list_id = save_data.get_data_old_id()

    url_start, url_q, url_end = url
    url_items = []
    for q in url_q:
        for status in url_end:
            url_items.append(f"{url_start}{q}&adst={status}&lst={status}")
    # Переходим на нужную страницу и ждем прогрузку + 5 секунд для загрущки JS.
    for i_url in url_items:
        driver.get(f"{i_url}&page=1")
        time.sleep(1)

        # Ниже полный цикл копирования номеров заказа и отправка их в список .
        while True:
            time.sleep(0.3)
            items_elements = driver.find_elements(By.CLASS_NAME, "m-sidebar__layout--found-item")
            if items_elements:
                for item in items_elements:
                    item_id = item.find_element(By.CLASS_NAME, "m-found-item__num")
                    id_str = (item_id.text)[2:]
                    if id_str not in items_id and id_str not in old_list_id:
                        items_id.append(id_str)
                    if id_str not in new_list_id:
                        new_list_id.append(id_str)
            
            # FIXME: На данный момент переход на следующие выполнен очень плохо и топорно, бывает падает и ловить баги... 
            # НО работает для v0.1.
            try:
                next_li = driver.find_element(
                    By.XPATH,
                    '//li[contains(@class,"page-item") and .//a[@aria-label="Next"]]'
                )

                # Нужен только для выхода со страницы.
                if "disabled" in next_li.get_attribute("class"): # type: ignore
                    break
                
                next_li.find_element(By.TAG_NAME, "a").click()
            except NoSuchElementException:
                break
    
    save_data.save_data_old_id(new_list_id)
    return items_id


def parser_local_site(*, site, items, driver: WebDriver) -> list[str]:
    """
    Парсим страницы заказов вызванные из функции parser_site и из списка items

    :return: Description
    :rtype: list[{str,str,str...}, {str,str,str...}...]
    """

    list_items = [] # Нужен только для сбора данных
    i = 0
    while i < len(items):
        # TODO: Создаем ссылку на сайт, переходим по этой ссылке.
        new_site = f"{site}/#/ext(popup:item/{items[i]}/advert)"
        driver.get(new_site)
        time.sleep(0.7)

        # FIXME: Сбор данных, можно изменить только переменные в будущем.
        try:
            item_id = (driver.find_element(By.CLASS_NAME, "m-modal__num").text)[2:]
        except NoSuchElementException:
            driver.refresh()
            time.sleep(3)
            continue
            
        name_product = driver.find_element(By.CLASS_NAME, "m-modal__title.m-title.m-title--h2.ng-star-inserted").text
        owner_product = (driver.find_element(By.CLASS_NAME, "m-infoblock__layout.ng-star-inserted").text)[9:]
        price_product = (driver.find_elements(By.CLASS_NAME, "m-infoblock__layout.ng-star-inserted")[1].text)[18:]
        
        try: 
            GlobalStart_date = driver.find_element(By.CLASS_NAME, "m-rangebox__layout")
            start_date = GlobalStart_date.find_element(By.CLASS_NAME, "m-rangebox__date.ng-star-inserted").text
        except NoSuchElementException:
            start_date = ""
        
        try:
            GlobalEnd_date = driver.find_element(By.CLASS_NAME, "m-rangebox__layout.m-rangebox__layout--rtl")
            end_date = GlobalEnd_date.find_element(By.CLASS_NAME, "m-rangebox__date.ng-star-inserted").text
        except NoSuchElementException:
            end_date = ""

        # Создаем удобный для нас список и отправляет его в глобальный массив данных.
        item = {"URL": new_site,
                "ID": item_id, 
                "START_DATE": start_date, 
                "END_DATE": end_date, 
                "NAME": name_product, 
                "OWNER": owner_product, 
                "PRICE": price_product
            }

        try:
            close_btn = driver.find_element(By.CLASS_NAME, "m-modal__close-button")
            close_btn.click()
        except NoSuchElementException:
            driver.refresh()
            time.sleep(3)
            continue
        except ElementClickInterceptedException:
            driver.refresh()
            time.sleep(3)
            continue

        list_items.append(item)
        i += 1

    return list_items


def main_parser(*, site, url) -> list[str]:
    #FIXME: Подключаем драйвер и сразу запускаем браузер. Долго
    driver = webdriver.Edge()
    WebDriverWait(driver, 10).until(lambda d: d.current_url is not None)

    # Сперва собираем данные номеров заказа.
    # Проходимся по номерам локально и собираем данные заказов там.
    items_list = parser_site(url=url, driver=driver)    
    items_data = parser_local_site(site=site, items=items_list, driver=driver)

    # Завершаем driver - закрываем браузер.
    # Смотрим данные и отправляем их назад.
    driver.quit()
    if items_data:
        return items_data
    return []

