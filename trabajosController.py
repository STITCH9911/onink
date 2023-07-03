import typing
from PyQt6 import QtCore
from views.trabajosIndex_ui import Ui_trabajosIndex
from PyQt6.QtWidgets import QWidget



class TrabajosIndex(QWidget, Ui_trabajosIndex):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.bt_tipos.clicked.connect(self.tipos_index)

    def tipos_index(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'tiposTrabajosIndex')
        w.search()
        sw.setCurrentWidget(w)