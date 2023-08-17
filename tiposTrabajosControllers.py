from typing import List, Tuple
from sqlalchemy.exc import IntegrityError
from config import Session
from models import TipoTrabajos
from strippedTable import StripedTable
from utils import BACK_ARROW, ICON_SAVE, PLUS, TIPOS_TRABAJOS_WHITE
from views.tiposTrabajosIndex_ui import Ui_tiposTrabajosIndex
from views.tiposTrabajosForm_ui import Ui_tiposTrabajosForm
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QSize
import os


class TiposTrabajosIndex(QWidget, Ui_tiposTrabajosIndex):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.le_search.textChanged.connect(self.search)
        self.table = None
        self.bt_create.clicked.connect(self.create)
        self.bt_create.setIcon(PLUS)
        self.search()
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

    def editFunc(self,obj):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'tiposTrabajosForm')
        w.setObjeto(obj)
        sw.setCurrentWidget(w)
    
    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "tiposTrabajosForm")
        sw.setCurrentWidget(w)
    
    def setItemsTable(self, objects):
        headers, data, dropdown_buttons, objects = self.getDataTable(objects)
        if self.table is not None:
            self.layout_tabla.removeWidget(self.table)
            self.table.clearContents()        
        self.table = StripedTable(headers, data, dropdown_buttons, objects)
        self.layout_tabla.addWidget(self.table)

    def search(self):
        le = self.le_search.text()
        with Session() as session:
            if le != "":
                items = session.query(TipoTrabajos).filter(TipoTrabajos.tipo.like(f"%{le}%")).all()
            else:
                items = session.query(TipoTrabajos).all()
        self.setItemsTable(items)

    def getDataTable(self, items: List['TipoTrabajos'])-> Tuple:
        with Session() as session:
            headers = ["Tipo de trabajo", "Opciones"]
            data = []
            
            dropdown_buttons = []
            
            for i in items:
                i = session.merge(i)
                data.append([i.tipo])
                dir = "views/images"
                size = QSize(30,30)
                edit = os.path.join(dir, 'edit-pencil.svg')
                trash = os.path.join(dir, 'trash.svg')
                buttons = [
                    {'Editar datos': self.editFunc, edit:size},
                    {'ELiminar': self.delete, trash:size},
                ]
                dropdown_buttons.append(buttons)
                
        return headers, data, dropdown_buttons, items
    
    def delete(self, obj):
        with Session() as session:
            obj = session.merge(obj)
            reply = QMessageBox.question(self.mainWindowWidget, "Advertencia", "Está a punto de eliminar un tipo de trabajo, si continúa no se podrá recuperar la información. ¿Desea continuar?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                session.delete(obj)
                session.commit()
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)

        self.search()
        

class TiposTrabajosForm(QWidget,Ui_tiposTrabajosForm):

    def __init__(self,parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_save.clicked.connect(self.save)
        self.bt_back.setIcon(BACK_ARROW)
        self.bt_save.setIcon(ICON_SAVE)
        self.bt_title.setIcon(TIPOS_TRABAJOS_WHITE)
        self.obj = None
        self.bt_back.clicked.connect(self.mostrar_widget)
        self.lineEdit.returnPressed.connect(self.save)
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

    def save(self):
        if self.lineEdit.text() == "":
            QMessageBox.warning(self.mainWindowWidget, "Advertencia", "Para llevar a cabo la acción debe llenar los campos correctamente", QMessageBox.StandardButton.Ok)
            return 

        with  Session() as session:
            if self.obj:
                self.obj = session.merge(self.obj)
                self.obj.tipo = self.lineEdit.text()
                session.add(self.obj)
            else:
                obj = TipoTrabajos(tipo=self.lineEdit.text())
                session.add(obj)
                            
            try:
                session.commit()
                self.mostrar_widget()
                self.lineEdit.clear()
                self.obj = None
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
            except IntegrityError:
                QMessageBox.critical(self.mainWindowWidget, "Error", "Ya existe este tipo de trabajo.", QMessageBox.StandardButton.Ok)
            

    def mostrar_widget(self):
        stackedWidget = self.parentWidget()
        w = stackedWidget.findChild(QWidget, "tiposTrabajosIndex")
        self.reload_data()
        stackedWidget.setCurrentWidget(w)
        self.lineEdit.clear()

    def reload_data(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "tiposTrabajosIndex")
        w.search()
        self.lineEdit.clear()
        
    def setObjeto(self,obj):
        self.obj = obj
        self.lineEdit.setText(obj.tipo)