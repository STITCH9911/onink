from typing import List, Tuple, Optional
from sqlalchemy.exc import IntegrityError
from PyQt6 import QtCore
from config import Session
from utils import BACK_ARROW, COUNTRY_WHITE, ICON_SAVE, PLUS
from views.paises_ui import Ui_PaisWidget
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import Qt, QSize
from strippedTable import StripedTable
from views.createPaises_ui import Ui_create_pais
from models import Paises
import os


class PaisesWidget(QWidget, Ui_PaisWidget):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.editFunc = None
        self.le_search_pais.textChanged.connect(self.search)
        self.table = None
        self.bt_add_pais.clicked.connect(self.create)
        self.bt_add_pais.setIcon(PLUS)
        self.search()
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

        

    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "create_pais")
        sw.setCurrentWidget(w)

        
    def set_functions(self, funcEdit):
        self.editFunc = funcEdit

    def setPaises(self, paises):
        headers, data, dropdown_buttons, countries = self.getDataTable(paises)
        if self.table is not None:
            self.layoutTablaPaises.removeWidget(self.table)
            self.table.clearContents()        
        self.table = StripedTable(headers, data, dropdown_buttons, countries)
        self.layoutTablaPaises.addWidget(self.table)




    def search(self):
        le = self.le_search_pais.text()
        with Session() as session:
            if le != "":
                paises = session.query(Paises).filter(Paises.pais.like(f"%{le}%")).all()
            else:
                paises = session.query(Paises).all()
        self.setPaises(paises)

    def getDataTable(self, paises: List['Paises'])-> Tuple:
        with Session() as session:
            headers = ["Pais", "Opciones"]
            data = []
            
            dropdown_buttons = []
            
            for p in paises:
                p = session.merge(p)
                data.append([p.pais])
                dir = "views/images"
                size = QSize(30,30)
                edit = os.path.join(dir, 'edit-pencil.svg')
                trash = os.path.join(dir, 'trash.svg')
                buttons = [
                    {'Editar datos': self.editFunc, edit:size},
                    {'ELiminar': self.delete, trash:size},
                ]
                dropdown_buttons.append(buttons)
                
        return headers, data, dropdown_buttons, paises
    
    def delete(self, obj):
        with Session() as session:
            obj = session.merge(obj)
            reply = QMessageBox.question(self.mainWindowWidget, "Advertencia", "Está a punto de eliminar un país, si continúa no se podrá recuperar la información. ¿Desea continuar?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                session.delete(obj)
                session.commit()
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
        
        self.search()
            




class PaisesWidgetCreate(QWidget,Ui_create_pais):

    def __init__(self,parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_save.clicked.connect(self.save)
        self.obj = None
        self.bt_back.clicked.connect(self.mostrar_widget)
        self.bt_back.setIcon(BACK_ARROW)
        self.bt_save.setIcon(ICON_SAVE)
        self.bt_title.setIcon(COUNTRY_WHITE)
        self.pais.returnPressed.connect(self.save)
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

    def set_functions(self, backFunc):
        self.bt_back.clicked.connect(backFunc)

    def save(self):
        if self.pais.text() == "":
            QMessageBox.critical(self.mainWindowWidget, "Error", "No pueden existir campos vacíos.", QMessageBox.StandardButton.Ok)
            return
        with  Session() as session:
            if self.obj:
                self.obj = session.merge(self.obj)
                self.obj.pais = self.pais.text()
                session.add(self.obj)
            elif not self.pais.text() == "":
                obj = Paises(pais=self.pais.text())
                session.add(obj)
            
            try:
                session.commit()
                self.mostrar_widget()
                self.pais.clear()
                self.obj = None
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
            except IntegrityError:
                QMessageBox.critical(self.mainWindowWidget, "Error", "Ya existe este país.", QMessageBox.StandardButton.Ok)
            

    def mostrar_widget(self):
        stackedWidget = self.parentWidget()
        w = stackedWidget.findChild(QWidget, "PaisWidget")
        self.recargar_datos_paises()
        stackedWidget.setCurrentWidget(w)

    def recargar_datos_paises(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "PaisWidget")
        w.search()

    def setPais(self,obj):
        self.obj = obj
        self.pais.setText(obj.pais)

