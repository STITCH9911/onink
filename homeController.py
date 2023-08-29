import typing
from PyQt6 import QtCore
from utils import BIRTHDAY, EYE
from views.home_ui import Ui_Home
from PyQt6.QtWidgets import QWidget

class Home(QWidget, Ui_Home):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
        self.bt_info.clicked.connect(self.showInfo)
        self.bt_cumple.clicked.connect(self.cumple)
        self.bt_info.setIcon(EYE)
        self.bt_cumple.setIcon(BIRTHDAY)

    def showInfo(self):
        p = self.parentWidget()
        w = p.findChild(QWidget, 'StatsDay')
        w.loadData()
        p.setCurrentWidget(w)

    def cumple(self):
        self.mainWindowWidget.cumple()