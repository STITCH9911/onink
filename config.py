from configparser import ConfigParser
import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

config = ConfigParser()
CONFIG_FILE_NAME = 'config.ini'
user_profile_dir = os.environ['USERPROFILE']
pictures_dir = os.path.join(user_profile_dir, 'Pictures')
PICTURES_DIR = pictures_dir
DEFAULT_PICTURE = "00000000000.png"
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
    if not os.path.isfile(CONFIG_FILE_NAME):
        config_create()
        print("Archivo de configuración creado correctamente")
    config.read(CONFIG_FILE_NAME)
    db = config.get('DATABASE', 'name')
    created = config.getboolean("DATABASE", 'created')
    return {'db': db, 'created': created}



db = get_config()["db"]
engine = create_engine(f"sqlite:///{db}")
Session = sessionmaker(bind=engine)