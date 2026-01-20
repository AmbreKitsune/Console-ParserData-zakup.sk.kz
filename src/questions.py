import exception_build

def type_for_purchase() -> str:
    """
    Запрос типа закупки.
    
    :return: Description
    :rtype: str | bool
    """
    print("Выберите что вы ищите: \n1 - Лоты\n2 - Закупки\n3 - Договоры (разработка)\nЛюбой не правильный ответ, выдаст ошибку!")
    tabs = input("Ваш ответ: ")
    match tabs:
        case "1":
            return "lot"
        case "2":
            return "advert"
        case "3":
            return "contractCard"
    raise exception_build.ErrorIncorrectType

def search_for_purchase() -> str:
    """
    Поиск предпочитаемого заказа(-ов)

    :return: Description
    :rtype: str
    """
    print("Слова для поиска или номер закупки? (можно пустой) (добавить несколько можно через запятую)")
    q = input("Ваш ответ: ")
    return q

def status_for_purchase() -> list[str]:
    """
    Выбор статуса заказа(-ов)
    
    :return: Description
    :rtype: list[str]
    """
    print("Выберите статус заказа(-ов): \n1 - Опубликовано\n2 - Опубликовано предварительное обсуждени\nЛюбой не правильный ответ, выдаст ошибку!")
    tabs = input("Ваш ответ: ").split(",")
    
    list_tabs = []
    for t in tabs:
        match t:
            case "1":
                list_tabs.append("PUBLISHED")
            case "2":
                list_tabs.append("DISCUSSION_PUBLISHED")
            case _:
                raise exception_build.ErrorIncorrectType
    return list_tabs

def services() -> str:
    """
    Выбор включен/выключение услуг в перечен заказа(-ов)
    
    :return: Description
    :rtype: str
    """
    print("Выключить услуги? (пустой = False): \n1 - Да\n2 - Нет")
    s = input("Ваш ответ: ")
    if s == "1":
        return "True" 
    return "False"

def work() -> str:
    """
    Выбор включен/выключение работ в перечен заказа(-ов)
    
    :return: Description
    :rtype: str
    """
    print("Выключить работы? (пустой = False): \n1 - Да\n2 - Нет")
    w = input("Ваш ответ: ")
    if w == "1":
        return "True"
    return "False"
