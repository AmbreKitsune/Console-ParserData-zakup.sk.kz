from config_builder import WorksConfigs
from parser import main_parser
from output import output
from logger import setup_logger

def main():
    """
    Входная точка для парсера.
    """
    logger = setup_logger()


    conf = WorksConfigs(logger=logger)
    conf.main_configs()
    site, url = conf.get_config()
    items: list = main_parser(logger=logger, site=site, url=url)
    output(items_list=items)

if __name__ == "__main__":
    main()
