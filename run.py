from .app.data.falsos import execute_falsos
import os
from .app.config import config_create

if __name__ == "__main__":
    if os.path.isfile('config.ini'):
        config_create()
    execute_falsos()