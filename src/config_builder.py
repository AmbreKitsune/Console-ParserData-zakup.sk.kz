import os
import configparser
import questions
import exception_build

FILENAME = "./config.ini"


def create_file_config() -> None:
    """
    Полготовка и создание config.ini.

    :return: Description
    :rtype: None
    """

    # Первичная настройка окружения. GLOBAL не изменяем, будущие изменение = ошибка + удаление файла при проверках и валидации.
    config = configparser.ConfigParser(allow_no_value=True)
    
    # FIXME: ДАННЫЕ ОТСЮДА, НЕ ИЗМЕНЯТЬ. БУДУ ЛОМАТЬ ПРОГРАММУ СРАЗУ!!!!
    config['GLOBAL'] = {
        "site": "https://zakup.sk.kz",
        "domen": "zakup.sk.kz"
    }

    config['EXT'] = {}
    
    # Спрашиваем тип запроса документов. Даёт STR | BOOL [False]. STR - продолжаем дальше. FALSE = ошибка и выход из системы.
    tabs = questions.type_for_purchase()
    config['EXT']['tabs'] = tabs # type: ignore

    # Вопросы: поиска документа, методы закупки, статусы, приоритеты и т.д 
    if tabs in ["lot", "advert"]:
        config['EXT']['q'] = questions.search_for_purchase()

        config['EXT']['s'] = questions.services()
        config['EXT']['w'] = questions.work()

        status_purchase = questions.status_for_purchase()
        config['EXT']['adst'] = status_purchase
        config['EXT']['lst'] = status_purchase
    else:
        # FIXME: заглушка, сразу уходим.
        raise exception_build.ErrorInWorking 

    # Записываем данные в ini для будущих запросов и быстрой подготовки данных по тем же запросам.
    with open(FILENAME, 'w', encoding="UTF-8") as file:
        config.write(file)

    print("Create config ini")


def reader_file_config() -> list[str]:
    """
    Читаем config.ini, выносим данные и превращаем это в ссылку.

    :return: Description
    :rtype: list[[str, str]...]
    """

    # Читаем файл конфига
    config = configparser.ConfigParser()
    files_read = config.read(FILENAME, encoding="UTF-8")
    
    # Если файла нет - ошибка,
    if not files_read:
        raise exception_build.ErrorMissingConfigFile
    

    # FIXME: Начинаем идти по config.ini и выносить данные от туда
    if not config.has_option('GLOBAL', 'site'):
        os.remove(FILENAME)
        raise exception_build.ErrorIncorrectData

    if not (site := config['GLOBAL']['site']):
        os.remove(FILENAME)
        raise exception_build.ErrorIncorrectData
 
    tabs = config['EXT']['tabs']
    q = config['EXT']['q']
    s = bool(config['EXT']['s'])
    w = bool(config['EXT']['w'])
    adst = config['EXT']['adst']
    lst = config['EXT']['lst']


    url = ""

    # Превращаем все переменные из данных, в одну больную ссылку для сайта.
    url += f"{site}/#/ext?"
    url += f"tabs={tabs}"
    if w:
        url += f"&w={w}"
    if s:
        url += f"&s={s}"
    if len(q) > 0:
        url += f"&q=" + "%20".join(q.split())
    url += f"&adst={adst}&lst={lst}"

    print("Reader config ini: DONE")
    return [site, url]


def check_file_config() -> list[str]:
    """
    Проверяем файл config.ini, если надо создаем и читаем.

    :return: Description
    :rtype: list[str, str]
    """

    # Провяраем наличие файла config.ini, если его нет - создаем.
    if not os.path.exists(FILENAME):
        create_file_config()
    
    # Читаем config.ini, получаем массив данных и отправляем его домой
    data = reader_file_config()
    if not data:
        raise exception_build.ErrorIncorrectData
    return data
