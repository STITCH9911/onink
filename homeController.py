import typing
from PyQt6 import QtCore
from views.home_ui import Ui_Home
from PyQt6.QtWidgets import QWidget

class Home(QWidget, Ui_Home):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.bt_info.clicked.connect(self.showInfo)

    def showInfo(self):
        p = self.parentWidget()
        w = p.findChild(QWidget, 'InfoDay')
        w.refresh()
        p.setCurrentWidget(w)