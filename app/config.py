import configparser

config = configparser.ConfigParser()

def config_create():
    config["DATABASE"] = {'name': "database.db", 'created': False}

    with open('config.ini', 'w') as f:
        config.write(f)

def set_config(section: str, atribute: str, value):
    config[section] = {atribute:value}


def get_config():
    config.read('config.ini')
    return {'db': config.get('DATABASE', 'name'), 'created': config.getboolean("DATABASE", 'created')}
