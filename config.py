import configparser
from const import CONFIG_FILE_NAME

config = configparser.ConfigParser()

def config_create():
    print("Creando archivo de configuración...")
    config["DATABASE"] = {'name': "database.db", 'created': False}
    with open(CONFIG_FILE_NAME, 'w') as f:
        config.write(f)

def set_config(seccion: str, atributo: str, valor):
    config.read(CONFIG_FILE_NAME)
    config.set(section=seccion, option=atributo, value=str(valor))
    with open(CONFIG_FILE_NAME, "w") as f:
        config.write(f)


def get_config():
    config.read(CONFIG_FILE_NAME)
    db = config.get('DATABASE', 'name')
    created = config.getboolean("DATABASE", 'created')
    return {'db': db, 'created': created}