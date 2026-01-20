from config_builder import WorksConfigs
from parser import main_parser
from output import output

def main():
    """
    Входная точка для парсера.
    """
    conf = WorksConfigs()
    conf.main_configs()
    site, url = conf.get_config()
    items: list = main_parser(site=site, url=url)
    output(items_list=items)

if __name__ == "__main__":
    main()
