import sys, traceback, logging
from app import Application
from datetime import datetime, date
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLibraryInfo, QLocale
from PyQt6.QtGui import QIcon
from gui import MainWindow
from config import get_config
import os

ruta_documentos = os.path.expanduser("~")
carpeta_logs = os.path.join(ruta_documentos, "OnInkLogs")
if not os.path.exists(carpeta_logs):
    os.makedirs(carpeta_logs)

nombre_archivo = f"{carpeta_logs}/log_{date.today().strftime('%Y-%m-%d')}.txt"
logging.basicConfig(filename=nombre_archivo, level=logging.ERROR)

def new_excepthook(type, value, tb):
    d = datetime.now()
    traceback.print_exception(type, value, tb)
    logging.exception(f"Excepcion de aplicacion\nFecha: {d.isoformat()}\n", exc_info=(type,value,tb))
    
sys.excepthook= new_excepthook

def main():
    app = Application()
    
    created = get_config()["created"]
    if not created:
        print("No existe base de datos\nProcediendo a crear base de datos...")
        from falsos import execute_falsos
        execute_falsos()
    qapp = QApplication(sys.argv)
    icon = QIcon(os.path.join('views/images', 'icon.ico')) 
    translator = QTranslator()
    translator.load(QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath) + "/qtbase_" + QLocale.system().name())
    qapp.setWindowIcon(icon)
    qapp.installTranslator(translator)
    gui = MainWindow(app)
    gui.setWindowIcon(icon)
    gui.show()
    sys.exit(qapp.exec())
    

if __name__ == '__main__':
    main()