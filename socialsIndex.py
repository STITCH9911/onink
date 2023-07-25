from typing import List, Tuple
from PyQt6 import QtCore
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from config import Session
from models import Socials, t_r_clients_socials
from strippedTable import StripedTable
from views.socials_ui import Ui_SocialsIndex
from views.createSocial_ui import Ui_socialCreate
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QSize
import os


class SocialsIndex(QWidget, Ui_SocialsIndex):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.le_search.textChanged.connect(self.search)
        self.table = None
        self.bt_create.clicked.connect(self.create)
        self.search()
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

    def editFunc(self,obj):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'socialCreate')
        w.setSocials(obj)
        sw.setCurrentWidget(w)
    
    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "socialCreate")
        sw.setCurrentWidget(w)
    
    def setSocials(self, socials):
        headers, data, dropdown_buttons, objects = self.getDataTable(socials)
        if self.table is not None:
            self.layout_tabla.removeWidget(self.table)
            self.table.clearContents()        
        self.table = StripedTable(headers, data, dropdown_buttons, objects)
        self.layout_tabla.addWidget(self.table)

    def search(self):
        le = self.le_search.text()
        with Session() as session:
            if le != "":
                socials = session.query(Socials).filter(Socials.social.like(f"%{le}%")).all()
            else:
                socials = session.query(Socials).all()
        self.setSocials(socials)

    def getDataTable(self, socials: List['Socials'])-> Tuple:
        with Session() as session:
            headers = ["Red social", "Opciones"]
            data = []
            
            dropdown_buttons = []
            
            for p in socials:
                p = session.merge(p)
                data.append([p.social])
                dir = "views/images"
                size = QSize(30,30)
                edit = os.path.join(dir, 'edit-pencil.svg')
                trash = os.path.join(dir, 'trash.svg')
                buttons = [
                    {'Editar datos': self.editFunc, edit:size},
                    {'ELiminar': self.delete, trash:size},
                ]
                dropdown_buttons.append(buttons)
                
        return headers, data, dropdown_buttons, socials
    
    def delete(self, obj):
        with Session() as session:
            obj = session.merge(obj)
            reply = QMessageBox.question(self.mainWindowWidget, "Advertencia", "Está a punto de eliminar una red social, si continúa no se podrá recuperar la información. ¿Desea continuar?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                stmp =  delete(t_r_clients_socials).where(t_r_clients_socials.c.social_id == obj.id)
                session.execute(stmp)
                session.delete(obj)
                session.commit()
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)

        self.search()
        



class SocialsWidgetCreate(QWidget,Ui_socialCreate):

    def __init__(self,parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_save.clicked.connect(self.save)
        self.obj = None
        self.bt_back.clicked.connect(self.mostrar_widget)
        self.social.returnPressed.connect(self.save)
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

    def save(self):
        if self.social.text() == "":
            QMessageBox.warning(self.mainWindowWidget, "Advertencia", "Para agregar un elemento nuevo debe llenar los campos correctamente", QMessageBox.StandardButton.Ok)
            return
        
        with  Session() as session:
            if self.obj:
                self.obj = session.merge(self.obj)
                self.obj.social = self.social.text()
                session.add(self.obj)
            elif not self.social.text() == "":
                obj = Socials(social=self.social.text())
                session.add(obj)
                
                            
            try:
                session.commit()
                self.mostrar_widget()
                self.social.clear()
                self.obj = None
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
            except IntegrityError:
                QMessageBox.critical(self.mainWindowWidget, "Error", "Ya existe esta red social.", QMessageBox.StandardButton.Ok)
            

    def mostrar_widget(self):
        stackedWidget = self.parentWidget()
        w = stackedWidget.findChild(QWidget, "SocialsIndex")
        self.recargar_datos_sociales()
        stackedWidget.setCurrentWidget(w)
        self.social.clear()

    def recargar_datos_sociales(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "SocialsIndex")
        w.search()
        self.social.clear()
        
    def setSocials(self,obj):
        self.obj = obj
        self.social.setText(obj.social)