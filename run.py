import os
from config import config_create, get_config, CONFIG_FILE_NAME
from main import main

if __name__ == "__main__":
    if not os.path.isfile(CONFIG_FILE_NAME):
        config_create()
        print("Archivo de configuración creado correctamente")
        db = get_config()["db"]
        if not os.path.isfile(db):
            print("No existe base de datos\nProcediendo a crear base de datos...")
            from falsos import execute_falsos
            execute_falsos()
    print("INICIANDO APLICACIÓN")
    main()