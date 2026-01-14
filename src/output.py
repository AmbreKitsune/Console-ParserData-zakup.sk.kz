import csv

def output(*, items_list: list):
    """
    Создание CSV файла из полученных данных.
    """
    
    data = [
        ['САЙТ', 'НОМЕР ПРОДУКТА', 'НАЧАЛО ПРИЁМА ЗАКАЗОВ', 'КОНЕЦ ПРИЁМА ЗАЯВОК', 'НАЗВАНИЕ ПРОДУКТА', 'ЗАКАЗЧИК ПРОДУКТА', 'ОБЩАЯ СУММА ЛОТОВ'],
    ]

    for item in items_list:
        data.append(item)

    with open('output_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
