import os

def get_data_old_id():
    if os.path.exists("save_id.txt"):
        with open("save_id.txt", "r", encoding="utf-8") as file:
            url_id = file.readline()

        return url_id.split(",")
    return []

def save_data_old_id(list_items):
    with open("save_id.txt", "w", encoding='UTF-8') as file:
        file.write(",".join(list_items))

