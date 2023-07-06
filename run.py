import os
from config import get_config, CONFIG_FILE_NAME
from main import main

if __name__ == "__main__":
    created = get_config()["created"]
    if not created:
        print("No existe base de datos\nProcediendo a crear base de datos...")
        from falsos import execute_falsos
        execute_falsos()
    main()