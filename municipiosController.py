from typing import List, Tuple
from PyQt6 import QtCore
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from config import Session
from models import Provincias, Municipios
from strippedTable import StripedTable
from utils import BACK_ARROW, ICON_SAVE, MUNICIPIOS_WHITE, PLUS, REFRESH
from views.municipios_ui import Ui_MunicipiosIndex
from views.municipiosForm_ui import Ui_MunicipiosForm
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QSize
import os


class MunicipiosIndex(QWidget, Ui_MunicipiosIndex):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_create.setIcon(PLUS)
        self.bt_refresh.setIcon(REFRESH)
        self.le_search.textChanged.connect(self.search)
        self.cb_provincia.currentIndexChanged.connect(self.search)
        self.table = None
        self.bt_create.clicked.connect(self.create)
        self.bt_refresh.clicked.connect(self.reload)
        self.search()
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

    def load_cb(self):
        with Session() as session:
            provincias = session.query(Provincias).all()
            if self.cb_provincia.count() != len(provincias):
                self.cb_provincia.clear()
                for item in provincias:
                    self.cb_provincia.addItem(item.provincia, item.id)
        self.cb_provincia.setCurrentIndex(-1)

    def reload(self):
        self.cb_provincia.setCurrentIndex(-1)
        self.le_search.clear()


    def editFunc(self,obj):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'MunicipiosForm')
        w.setObjeto(obj)
        sw.setCurrentWidget(w)
    
    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "MunicipiosForm")
        w.load_cb()
        sw.setCurrentWidget(w)
    
    def setLista(self, lista):
        headers, data, dropdown_buttons, objects = self.getDataTable(lista)
        if self.table is not None:
            self.layout_tabla.removeWidget(self.table)
            self.table.clearContents()        
        self.table = StripedTable(headers, data, dropdown_buttons, objects)
        self.layout_tabla.addWidget(self.table)

    def search(self):
        le = self.le_search.text()
        with Session() as session:
            lista = session.query(Municipios)
            if le != "":
                lista = lista.filter(Municipios.municipio.like(f"%{le}%"))
            if self.cb_provincia.currentIndex() != -1:
                data = self.cb_provincia.currentData()
                lista  = lista.filter(Municipios.provincia_id == data)
            lista = lista.all()
        self.setLista(lista)

    def getDataTable(self, lista: List['Municipios'])-> Tuple:
        with Session() as session:
            headers = ["Municipio", "Provincia", "Opciones"]
            data = []
            
            dropdown_buttons = []
            
            for item in lista:
                item = session.merge(item)
                data.append([item.municipio, item.provincia.provincia])
                dir = "views/images"
                size = QSize(30,30)
                edit = os.path.join(dir, 'edit-pencil.svg')
                trash = os.path.join(dir, 'trash.svg')
                buttons = [
                    {'Editar datos': self.editFunc, edit:size},
                    {'ELiminar': self.delete, trash:size},
                ]
                dropdown_buttons.append(buttons)
                
        return headers, data, dropdown_buttons, lista
    
    def delete(self, obj):
        with Session() as session:
            obj = session.merge(obj)
            reply = QMessageBox.question(self.mainWindowWidget, "Advertencia", "Está a punto de eliminar un municipio, si continúa no se podrá recuperar la información. ¿Desea continuar?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                session.delete(obj)
                session.commit()
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
        self.load_cb()
        self.search()
        



class MunicipiosForm(QWidget,Ui_MunicipiosForm):

    def __init__(self,parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_save.clicked.connect(self.save)
        self.bt_back.setIcon(BACK_ARROW)
        self.bt_save.setIcon(ICON_SAVE)
        self.pushButton.setIcon(MUNICIPIOS_WHITE)
        self.obj = None
        self.bt_back.clicked.connect(self.mostrar_widget)
        self.municipio.returnPressed.connect(self.save)
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

    def save(self):
        if self.municipio.text() == "" or self.cb_provincia.currentIndex() == -1:
            QMessageBox.warning(self.mainWindowWidget, "Advertencia", "Para llevar a cabo la acción debe llenar los campos correctamente", QMessageBox.StandardButton.Ok)
            return 

        with  Session() as session:
            if self.obj:
                self.obj = session.merge(self.obj)
                self.obj.municipio = self.municipio.text()
                self.obj.provincia_id = self.cb_provincia.currentData()
                session.add(self.obj)
            else:
                obj = Municipios(municipio = self.municipio.text(),provincia_id=self.cb_provincia.currentData())
                session.add(obj)
            
            try:
                session.commit()
                self.mostrar_widget()
                self.municipio.clear()
                self.cb_provincia.setCurrentIndex(-1)
                self.obj = None
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
            except IntegrityError:
                QMessageBox.critical(self.mainWindowWidget, "Error", "Ya existe este municipio.", QMessageBox.StandardButton.Ok)
            

    def mostrar_widget(self):
        stackedWidget = self.parentWidget()
        w = stackedWidget.findChild(QWidget, "MunicipiosIndex")
        self.recargar_datos_index()
        stackedWidget.setCurrentWidget(w)
        self.municipio.clear()
        self.cb_provincia.setCurrentIndex(-1)

    def recargar_datos_index(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "MunicipiosIndex")
        w.search()
        self.municipio.clear()
        self.cb_provincia.setCurrentIndex(-1)
        
    def setObjeto(self,obj):
        self.load_cb()
        self.obj = obj
        self.municipio.setText(obj.municipio)
        index = self.cb_provincia.findData(obj.provincia_id)
        self.cb_provincia.setCurrentIndex(index)

    def load_cb(self):
        with Session() as session:
            provincias = session.query(Provincias).all()
            if self.cb_provincia.count() != len(provincias):
                self.cb_provincia.clear()
                for item in provincias:
                    self.cb_provincia.addItem(item.provincia, item.id)
        self.cb_provincia.setCurrentIndex(-1)
                