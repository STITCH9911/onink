import os
from sqlalchemy import create_engine
from config import get_config
from sqlalchemy.orm.session import sessionmaker

CONFIG_FILE_NAME = 'config.ini'

if os.path.isfile(CONFIG_FILE_NAME):
    db = get_config()["db"]
    engine = create_engine(f"sqlite:///{db}")
    Session = sessionmaker(bind=engine)