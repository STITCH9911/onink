from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QPushButton, QMenu, QAbstractScrollArea, QHeaderView
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize
import os
style = """

QTableWidget::item {
    color: white;
}

QTableWidget::item:alternate {
    color: black;
}
QPushButton::menu-indicator { 
    padding: 0;
    image: none; qproperty-iconAlignment: 'center';
}
"""


class StripedTable(QTableWidget):
    def __init__(self, headers, data, buttons, objects, parent=None):
        super().__init__(parent)
        self.setColumnCount(len(headers) + 1)
        if data:
            self.setRowCount(len(data))
            self.setHorizontalHeaderLabels(['No.', *headers])
            self.verticalHeader().setVisible(False)
            self.setAlternatingRowColors(True)
            self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.populate_table(data, buttons, objects)
        else:
            self.setRowCount(2)
            self.horizontalHeader().setVisible(False)
            self.setVerticalHeaderLabels(['', ''])
            self.setSpan(0, 0, 2, len(headers) + 1)
            item = QTableWidgetItem('Sin resultados')
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(0, 0, item)
        self.setStyleSheet(style)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def populate_table(self, data, buttons, objects):
        for i, row in enumerate(data):
            first_item = QTableWidgetItem(str(i+1))
            first_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(i, 0,first_item)
            for j, item in enumerate(row):
                table_item =  QTableWidgetItem(item)
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(i, j + 1,table_item)
            self.setCellWidget(i, len(row) + 1, self.create_dropdown_button(buttons[i], objects[i]))
            self.cellWidget(i, len(row) + 1).setStyleSheet(f"background-color:rgb({self.item(i,0).background().color().getRgb()})")
    def create_dropdown_button(self, button_data, obj):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        button_menu = QMenu()
        button_menu.setStyleSheet("QMenu::indicator { width:0px; }")
        button = QPushButton("")
        button.setIcon(QIcon(os.path.join('images','menu-horizontal.svg')))
        button.setIconSize(QSize(30,20))
        button.setFlat(True)
        for btn in button_data:
            for button_text, button_func in btn.items():
                action = QAction(button_text, self)
                action.triggered.connect(lambda checked, x=obj, func=button_func: func(x))
                button_menu.addAction(action)  # Agregar la acción al menú
        button.setMenu(button_menu)
        button.setStyleSheet('padding: 0px; border: none;')
        layout.addWidget(button)
        layout.setAlignment(button, Qt.AlignmentFlag.AlignCenter)
        return widget