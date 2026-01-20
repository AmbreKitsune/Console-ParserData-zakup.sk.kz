import os
import configparser
import questions
import exception_build


class WorksConfigs:
    def __init__(self) -> None:
        self.file_name: str | None = None
        self.type_configs: str | None = None
        self.site: str | None = None
        self.url: str | None = None

        self.url_start: str | None = None
        self.url_q: list | None = None
        self.url_end: list | None = None

    def main_configs(self) -> None:
        """
        Проверяем файл config.ini, если надо создаем и читаем.
        """

        while self.file_name is None:
            self.type_configs = self.check_file_config()
            
            if self.type_configs == "Folder":
                self.work_in_folder_configs()

            if self.type_configs == "Create":
                self.choosing_create_file_or_folder()

        print(self.file_name)
        self.reader_file_config()
        
        
    def check_file_config(self):
        if os.path.exists(".\\configs"):
            return "Folder"
        if os.path.exists(".\\config.ini"):
            self.file_name = ".\\config.ini"
            return "File" 
        return "Create"

    def choosing_create_file_or_folder(self):
        print("Создание конфига(-ов):" \
            "\n1 - Создать один конфиг" \
            "\n2 - Создать папку для конфига"
        )
        result = int(input("Выбор:"))
        
        match result:
            case 1:
                self.file_name = ".\\config.ini"
                self.create_file_config()
            case 2:
                self.create_folders_configs()
            case _:
                pass

    def create_file_config(self) -> None:
        """
        Подготовка и создание config.ini.
        """

        # Первичная настройка окружения. GLOBAL не изменяем, будущие изменение = ошибка + удаление файла при проверках и валидации.
        config = configparser.ConfigParser(allow_no_value=True)
        
        # TODO: ДАННЫЕ ОТСЮДА, НЕ ИЗМЕНЯТЬ. БУДУ ЛОМАТЬ ПРОГРАММУ СРАЗУ!!!!
        config['GLOBAL'] = {
            "site": "https://zakup.sk.kz",
            "domain": "zakup.sk.kz"
        }

        config['EXT'] = {}
        
        # Спрашиваем тип запроса документов. Даёт STR | BOOL [False]. STR - продолжаем дальше. FALSE = ошибка и выход из системы.
        tabs: str = questions.type_for_purchase()
        config['EXT']['tabs'] = tabs

        # Вопросы: поиска документа, методы закупки, статусы, приоритеты и т.д 
        if tabs in ["lot", "advert"]:
            config['EXT']['q'] = questions.search_for_purchase()

            config['EXT']['s'] = questions.services()
            config['EXT']['w'] = questions.work()

            status_purchase = questions.status_for_purchase()
            config['EXT']['adst'] = ",".join(status_purchase)
            config['EXT']['lst'] = ",".join(status_purchase)
        else:
            # FIXME: заглушка, сразу уходим.
            raise exception_build.ErrorInWorking 

        # Записываем данные в ini для будущих запросов и быстрой подготовки данных по тем же запросам.
        with open(self.file_name, 'w', encoding="UTF-8") as file: # type: ignore
            config.write(file)


    def create_folders_configs(self) -> None:
        """
        Создание папки для конфига и создание конфига в нём
        """

        # Создание папки
        if not os.path.exists(".\\configs"):
            os.mkdir(".\\configs")
        
        # Подключение конфига
        config = configparser.ConfigParser(allow_no_value=True)
        
        # TODO: ДАННЫЕ ОТСЮДА, НЕ ИЗМЕНЯТЬ. БУДУ ЛОМАТЬ ПРОГРАММУ СРАЗУ!!!!
        config['GLOBAL'] = {
            "site": "https://zakup.sk.kz",
            "domain": "zakup.sk.kz"
        }

        config['EXT'] = {}
        
        # Спрашиваем тип запроса документов. Даёт STR | BOOL [False]. STR - продолжаем дальше. FALSE = ошибка и выход из системы.
        tabs: str = questions.type_for_purchase()
        config['EXT']['tabs'] = tabs

        # Вопросы: поиска документа, методы закупки, статусы, приоритеты и т.д 
        if tabs in ["lot", "advert"]:
            q = questions.search_for_purchase()
            list_q = q.split(',')
            config['EXT']['q'] = q

            config['EXT']['s'] = questions.services()
            config['EXT']['w'] = questions.work()

            status_purchase = questions.status_for_purchase()
            config['EXT']['adst'] = ",".join(status_purchase)
            config['EXT']['lst'] = ",".join(status_purchase)
        else:
            # FIXME: заглушка, сразу уходим.
            raise exception_build.ErrorInWorking 

        # Записываем данные в ini для будущих запросов и быстрой подготовки данных по тем же запросам.
        file_name = f".\\configs\\{"_".join(list_q)}"
        
        if os.path.exists(file_name):
            return
        os.mkdir(file_name)
        
        with open(f"{file_name}\\config.ini", 'w', encoding="UTF-8") as file: # type: ignore
            config.write(file)

    def work_in_folder_configs(self):
        content = os.listdir(".\\configs")
        if not content:
            os.rmdir(".\\configs")
            return
        
        items= []
        print("Список всех доступных конфиг файлов!")
        print("0 - Создать конфиг файл")
        for index, item in enumerate(content):
            full_path = os.path.join(".\\configs", item)
            if os.path.isdir(full_path):
                items.append([item, full_path])
                print(f"{index+1} - {item}")
            
        index = int(input("Выберите число: "))
        if index == 0:
            self.type_configs = "Create"
            return
        self.file_name = f"{items[index-1][1]}\\config.ini"

    def reader_file_config(self):
        """
        Читаем config.ini, выносим данные и превращаем это в ссылку.
        """

        # Читаем файл конфига
        config = configparser.ConfigParser()
        files_read = config.read(self.file_name, encoding="UTF-8") # type: ignore
        
        # Если файла нет - ошибка,
        if not files_read:
            raise exception_build.ErrorMissingConfigFile
        

        # FIXME: Начинаем идти по config.ini и выносить данные от туда
        if not config.has_option('GLOBAL', 'site'):
            os.remove(self.file_name) # type: ignore
            raise exception_build.ErrorIncorrectData

        self.site = config['GLOBAL']['site']
        if not (self.site):
            os.remove(self.file_name) # type: ignore
            raise exception_build.ErrorIncorrectData
    

        tabs = config['EXT']['tabs']
        q = config['EXT']['q'].split(",")
        s = bool(config['EXT']['s'])
        w = bool(config['EXT']['w'])
        adst_lst = config['EXT']['adst']

        # Превращаем все переменные из данных, в одну больную ссылку для сайта.
        self.url_start = f"{self.site}/#/ext?"
        self.url_start += f"tabs={tabs}"
        if w:
            self.url_start += f"&w={w}"
        if s:
            self.url_start += f"&s={s}"
        
        self.url_q = []
        for i in q:
            self.url_q.append(f"&q={'%20'.join(i.split())}")
        
        self.url_end = adst_lst.split(",")
        # url_end = f"&adst={adst}&lst={lst}"

        print("Reader config ini: DONE")
    
    def get_config(self):
        return [self.site, [self.url_start, self.url_q, self.url_end]]



