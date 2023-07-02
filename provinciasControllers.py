from typing import List, Tuple
from PyQt6 import QtCore
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from config import Session
from models import Provincias
from strippedTable import StripedTable
from views.provincias_ui import Ui_ProvinciaIndex
from views.provinciaForm_ui import Ui_provinciasForm
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QSize
import os


class ProvinciasIndex(QWidget, Ui_ProvinciaIndex):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.le_search.textChanged.connect(self.search)
        self.table = None
        self.bt_create.clicked.connect(self.create)
        self.search()

    def editFunc(self,obj):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'provinciasForm')
        w.setObjeto(obj)
        sw.setCurrentWidget(w)
    
    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "provinciasForm")
        sw.setCurrentWidget(w)
    
    def setProvincias(self, provincias):
        headers, data, dropdown_buttons, objects = self.getDataTable(provincias)
        if self.table is not None:
            self.layout_tabla.removeWidget(self.table)
            self.table.clearContents()        
        self.table = StripedTable(headers, data, dropdown_buttons, objects)
        self.layout_tabla.addWidget(self.table)

    def search(self):
        le = self.le_search.text()
        with Session() as session:
            if le != "":
                provincias = session.query(Provincias).filter(Provincias.provincia.like(f"%{le}%")).all()
            else:
                provincias = session.query(Provincias).all()
        self.setProvincias(provincias)

    def getDataTable(self, provincias: List['Provincias'])-> Tuple:
        with Session() as session:
            headers = ["Provincia", 'Cant. de Municipios', "Opciones"]
            data = []
            
            dropdown_buttons = []
            
            for p in provincias:
                p = session.merge(p)
                data.append([p.provincia, str(len(p.municipios))])
                dir = "views/images"
                size = QSize(30,30)
                edit = os.path.join(dir, 'edit-pencil.svg')
                trash = os.path.join(dir, 'trash.svg')
                buttons = [
                    {'Editar datos': self.editFunc, edit:size},
                    {'ELiminar': self.delete, trash:size},
                ]
                dropdown_buttons.append(buttons)
                
        return headers, data, dropdown_buttons, provincias
    
    def delete(self, obj):
        with Session() as session:
            obj = session.merge(obj)
            reply = QMessageBox.question(self, "Advertencia", "Está a punto de eliminar una red provincia, si continúa no se podrá recuperar la información. ¿Desea continuar?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                session.delete(obj)
                session.commit()
                QMessageBox.information(self, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)

        self.search()
        



class ProvinciasForm(QWidget,Ui_provinciasForm):

    def __init__(self,parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_save.clicked.connect(self.save)
        self.obj = None
        self.bt_back.clicked.connect(self.mostrar_widget)
        self.provincia.returnPressed.connect(self.save)

    def save(self):
        if self.provincia.text() == "":
            QMessageBox.warning(self, "Advertencia", "Para llevar a cabo la acción debe llenar los campos correctamente", QMessageBox.StandardButton.Ok)
            return 

        with  Session() as session:
            if self.obj:
                self.obj = session.merge(self.obj)
                self.obj.provincia = self.provincia.text()
                session.add(self.obj)
            else:
                obj = Provincias(provincia=self.provincia.text())
                session.add(obj)
                            
            try:
                session.commit()
                self.mostrar_widget()
                self.provincia.clear()
                self.obj = None
                QMessageBox.information(self, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
            except IntegrityError:
                QMessageBox.critical(self, "Error", "Ya existe esta provincia.", QMessageBox.StandardButton.Ok)
            

    def mostrar_widget(self):
        stackedWidget = self.parentWidget()
        w = stackedWidget.findChild(QWidget, "ProvinciaIndex")
        self.recargar_datos_sociales()
        stackedWidget.setCurrentWidget(w)
        self.provincia.clear()

    def recargar_datos_sociales(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "ProvinciaIndex")
        w.search()
        self.provincia.clear()
        
    def setObjeto(self,obj):
        self.obj = obj
        self.provincia.setText(obj.provincia)