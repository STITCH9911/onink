import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

config = configparser.ConfigParser()
CONFIG_FILE_NAME = 'config.ini'

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

if os.path.isfile(CONFIG_FILE_NAME):
    db = get_config()["db"]
    engine = create_engine(f"sqlite:///{db}")
    Session = sessionmaker(bind=engine)