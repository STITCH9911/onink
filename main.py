import sys, traceback
from app import Application

def new_excepthook(type, value, tb):
    traceback.print_exception(type, value, tb)
sys.excepthook= new_excepthook

def main():
    app = Application()
    from PyQt6.QtWidgets import QApplication
    from gui import MainWindow
    qapp = QApplication(sys.argv)
    gui = MainWindow(app)
    gui.show()
    sys.exit(qapp.exec())

if __name__ == '__main__':
    main()