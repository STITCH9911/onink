from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QPushButton, QMenu, QAbstractScrollArea, QHeaderView
from PyQt6.QtGui import QAction, QIcon, QCursor, QFont, QColor
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtCore import QCoreApplication
import os

_translate = QCoreApplication.translate
style = """

QTableWidget::item {
    color: white;
    font-size: 12pt;
}

QTableWidget::item:alternate {
    color: white;
    font-size: 12pt;
    
}
QPushButton::menu-indicator { 
    padding: 0;
    image: none; qproperty-iconAlignment: 'center';
}
QPushButton:hover{
background-color: rgb(128,128,128);
border-radius: 20;
}
QScrollBar:vertical {
	background-color: rgb(235, 235, 235);
        width: 10px;
        margin: 0px 0 0px 0;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical {
	background-color: rgb(243, 156, 18);
        min-height: 20px;
        border-radius: 5px;
    }

    QScrollBar::add-line:vertical {
        background-color: #F5F5F5;
        height: 0px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
    }

    QScrollBar::sub-line:vertical {
        background-color: #F5F5F5;
        height: 0px;
        subcontrol-position: top;
        subcontrol-origin: margin;
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background-color: none;
    }

"""
COLOR_PAR = QColor(100,100,100)
COLOR_IMPAR = QColor(60,60,60)

class StripedTable(QTableWidget):
    def __init__(self, headers, data, buttons, objects, parent=None):
        super().__init__(parent)
        self.setObjectName('Tabla')
        self.setColumnCount(len(headers) + 1)
        if data:
            self.setRowCount(len(data))
            self.setHorizontalHeaderLabels(['No.', *headers])
            self.horizontalHeader().setFont(QFont('Oswald', 12))
            self.verticalHeader().setVisible(False)
            self.setAlternatingRowColors(True)
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
        self.horizontalHeader().setSectionResizeMode(self.columnCount() - 1, QHeaderView.ResizeMode.ResizeToContents)
        self.resizeRowsToContents()
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

    def populate_table(self, data, buttons, objects):
        for i, row in enumerate(data):
            first_item = QTableWidgetItem(str(i+1))
            first_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            first_item.setFont(QFont('Oswald', 12))
            self.setItem(i, 0,first_item)
            first_item.setSizeHint(QSize(50,70))
            if i % 2 == 0:
                self.item(i,0).setBackground(COLOR_PAR)
            else:
                self.item(i,0).setBackground(COLOR_IMPAR)
            for j, item in enumerate(row):
                table_item =  QTableWidgetItem(item)
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table_item.setFont(QFont('Oswald', 12))
                self.setItem(i, j + 1,table_item)
                if i % 2 == 0:
                    self.item(i,j + 1).setBackground(COLOR_PAR)
                else:
                    self.item(i,j + 1).setBackground(COLOR_IMPAR)
            if len(buttons) > 0:
                self.setCellWidget(i, len(row) + 1, self.create_dropdown_button(buttons[i], objects[i]))
                self.cellWidget(i, len(row) + 1).setStyleSheet(f"background-color:rgba{self.item(i,0).background().color().getRgb()};")
    def create_dropdown_button(self, button_data, obj):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        button_menu = QMenu()
        button_menu.setStyleSheet("QMenu::indicator { width:0px; } QMenu{ font-size: 12pt;}")
        button = QPushButton("")
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.setIcon(QIcon(os.path.join('views/images','options2.svg')))
        button.setToolTip(_translate("OnInkMainWindow", "<html><head/><body><p style=\" background-color:white; \"><span style=\" font-size:9pt; font-weight:600;  background-color:white;\">Opciones</span></p></body></html>"))
        button.setIconSize(QSize(20,20))
        #button.setFlat(True)
        for btn in button_data:
            b, i = btn.items()
            button_text, button_func = b
            iconFileName, iconSize = i
            action = QAction(button_text, self)
            icon = QIcon()
            icon.addFile(iconFileName, iconSize)
            action.setIcon(icon)
            action.triggered.connect(lambda checked, x=obj, func=button_func: func(x))
            button_menu.addAction(action)  # Agregar la acción al menú
        button.setMenu(button_menu)
        button.setStyleSheet('padding: 0px; border: none;')
        layout.addWidget(button)
        layout.setAlignment(button, Qt.AlignmentFlag.AlignCenter)
        return widget