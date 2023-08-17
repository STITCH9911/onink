from typing import List, Tuple
from PyQt6 import QtCore
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from config import Session
from models import Tonalidades
from strippedTable import StripedTable
from utils import BACK_ARROW, ICON_SAVE, PLUS, TONOS_WHITE
from views.tonos_ui import Ui_TonosWidget
from views.TonoForm_ui import Ui_TonoForm
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QSize
import os


class TonosIndex(QWidget, Ui_TonosWidget):
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
        w = sw.findChild(QWidget, 'TonoForm')
        w.setObjeto(obj)
        sw.setCurrentWidget(w)
    
    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "TonoForm")
        sw.setCurrentWidget(w)
    
    def setItemsTable(self, objects):
        headers, data, dropdown_buttons, objects = self.getDataTable(objects)
        if self.table is not None:
            self.layoutTabla.removeWidget(self.table)
            self.table.clearContents()        
        self.table = StripedTable(headers, data, dropdown_buttons, objects)
        self.layoutTabla.addWidget(self.table)

    def search(self):
        le = self.le_search.text()
        with Session() as session:
            if le != "":
                items = session.query(Tonalidades).filter(Tonalidades.tono.like(f"%{le}%")).all()
            else:
                items = session.query(Tonalidades).all()
        self.setItemsTable(items)

    def getDataTable(self, items: List['Tonalidades'])-> Tuple:
        with Session() as session:
            headers = ["Tono", "Opciones"]
            data = []
            
            dropdown_buttons = []
            
            for i in items:
                i = session.merge(i)
                data.append([i.tono])
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
            reply = QMessageBox.question(self.mainWindowWidget, "Advertencia", "Está a punto de eliminar un tono, si continúa no se podrá recuperar la información. ¿Desea continuar?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                session.delete(obj)
                session.commit()
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)

        self.search()
        



class TonoForm(QWidget,Ui_TonoForm):

    def __init__(self,parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_save.clicked.connect(self.save)
        self.obj = None
        self.bt_back.setIcon(BACK_ARROW)
        self.bt_save.setIcon(ICON_SAVE)
        self.bt_title.setIcon(TONOS_WHITE)
        self.bt_back.clicked.connect(self.mostrar_widget)
        self.tono.returnPressed.connect(self.save)
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
        

    def save(self):
        if self.tono.text() == "":
            QMessageBox.warning(self.mainWindowWidget, "Advertencia", "Para llevar a cabo la acción debe llenar los campos correctamente", QMessageBox.StandardButton.Ok)
            return 

        with  Session() as session:
            if self.obj:
                self.obj = session.merge(self.obj)
                self.obj.tono = self.tono.text()
                session.add(self.obj)
            else:
                obj = Tonalidades(tono=self.tono.text())
                session.add(obj)
                            
            try:
                session.commit()
                self.mostrar_widget()
                self.tono.clear()
                self.obj = None
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
            except IntegrityError:
                QMessageBox.critical(self.mainWindowWidget, "Error", "Ya existe este tono.", QMessageBox.StandardButton.Ok)
            

    def mostrar_widget(self):
        stackedWidget = self.parentWidget()
        w = stackedWidget.findChild(QWidget, "TonosWidget")
        self.reload_data()
        stackedWidget.setCurrentWidget(w)
        self.tono.clear()

    def reload_data(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "TonosWidget")
        w.search()
        self.tono.clear()
        
    def setObjeto(self,obj):
        self.obj = obj
        self.tono.setText(obj.tono)