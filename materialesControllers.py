from typing import List, Tuple
from sqlalchemy.exc import IntegrityError
from config import Session
from models import Materiales
from strippedTable import StripedTable
from utils import BACK_ARROW, ICON_SAVE, MATERIALS_WHITE, PLUS
from views.materialesIndex_ui import Ui_materialesIndex
from views.materialesForm_ui import Ui_materialesForm
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QDoubleValidator
import os, re


class MaterialIndex(QWidget, Ui_materialesIndex):
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
        w = sw.findChild(QWidget, 'materialesForm')
        w.setObjeto(obj)
        sw.setCurrentWidget(w)
    
    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "materialesForm")
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
            items = session.query(Materiales)
            if le != "":
                if le.isdigit():
                    items = items.filter(Materiales.costo.like(f"%{le}%"))
                else:
                    items = items.filter(Materiales.material.like(f"%{le}%"))
            items = items.all()
        self.setItemsTable(items)

    def getDataTable(self, items: List['Materiales'])-> Tuple:
        with Session() as session:
            headers = ["Material","Costo", "Opciones"]
            data = []
            dropdown_buttons = []
            
            for i in items:
                i = session.merge(i)
                data.append([i.material, str(i.costo)])
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
            reply = QMessageBox.question(self.mainWindowWidget, "Advertencia", "Está a punto de eliminar un material, si continúa no se podrá recuperar la información. ¿Desea continuar?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                session.delete(obj)
                session.commit()
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)

        self.search()
        

class MaterialForm(QWidget,Ui_materialesForm):

    def __init__(self,parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_back.setIcon(BACK_ARROW)
        self.bt_title.setIcon(MATERIALS_WHITE)
        self.bt_save.setIcon(ICON_SAVE)
        self.bt_save.clicked.connect(self.save)
        self.obj = None
        self.bt_back.clicked.connect(self.mostrar_widget)
        self.lineEdit.returnPressed.connect(self.save)
        self.costo.setValidator(QDoubleValidator())
        self.costo.textChanged.connect(self.validate_costo)
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
    
    def validate_costo(self, text):
        regex = re.compile(r"^(\d*\.?\d*)$")
        match = regex.search(text)
        if not match:
            self.costo.setText(text[:-1])

    def save(self):
        if self.lineEdit.text() == "" or self.costo.text() == "":
            QMessageBox.warning(self.mainWindowWidget, "Advertencia", "Para llevar a cabo la acción debe llenar los campos correctamente", QMessageBox.StandardButton.Ok)
            return 

        with  Session() as session:
            if self.obj:
                self.obj = session.merge(self.obj)
                self.obj.material = self.lineEdit.text()
                self.obj.costo = self.costo.text()
                session.add(self.obj)
            else:
                obj = Materiales(material=self.lineEdit.text(), costo=self.costo.text())
                session.add(obj)
                            
            try:
                session.commit()
                self.mostrar_widget()
                self.lineEdit.clear()
                self.costo.clear()
                self.obj = None
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
            except IntegrityError:
                QMessageBox.critical(self.mainWindowWidget, "Error", "Ya existe este material.", QMessageBox.StandardButton.Ok)
            

    def mostrar_widget(self):
        stackedWidget = self.parentWidget()
        w = stackedWidget.findChild(QWidget, "materialesIndex")
        self.reload_data()
        stackedWidget.setCurrentWidget(w)
        self.lineEdit.clear()
        self.costo.clear()

    def reload_data(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "materialesIndex")
        w.search()
        self.lineEdit.clear()
        self.costo.clear()
        
    def setObjeto(self,obj):
        self.obj = obj
        self.lineEdit.setText(obj.material)
        self.costo.setText(str(obj.costo))