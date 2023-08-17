import typing
from PyQt6 import QtCore
from utils import EYE
from views.home_ui import Ui_Home
from PyQt6.QtWidgets import QWidget

class Home(QWidget, Ui_Home):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.bt_info.clicked.connect(self.showInfo)
        self.bt_info.setIcon(EYE)

    def showInfo(self):
        p = self.parentWidget()
        w = p.findChild(QWidget, 'StatsDay')
        w.loadData()
        p.setCurrentWidget(w)