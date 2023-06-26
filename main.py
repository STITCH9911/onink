import sys, traceback, logging
from app import Application

logging.basicConfig(filename='log.txt', level=logging.ERROR)

def new_excepthook(type, value, tb):
    traceback.print_exception(type, value, tb)
    logging.exception("Excepción de aplicación", exc_info=(type,value,tb))
    
sys.excepthook= new_excepthook

def main():
    app = Application()
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QTranslator, QLibraryInfo, QLocale
    from gui import MainWindow
    qapp = QApplication(sys.argv)
    translator = QTranslator()
    translator.load(QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath) + "/qtbase_" + QLocale.system().name())
    qapp.installTranslator(translator)
    gui = MainWindow(app)
    gui.show()
    sys.exit(qapp.exec())
    

if __name__ == '__main__':
    main()