from typing import List, Tuple
from config import Session
from datetime import datetime
from views.trabajosIndex_ui import Ui_trabajosIndex
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QSize
from models import Trabajos
import os


class TrabajosIndex(QWidget, Ui_trabajosIndex):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_tipos.clicked.connect(self.tipos_index)
        self.le_search.textChanged.connect(self.search)
        self.bt_create.clicked.connect(self.create)
        self.search()

    def tipos_index(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'tiposTrabajosIndex')
        w.search()
        sw.setCurrentWidget(w)

    def search(self):
        pass

    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'trabajosForm')
        sw.setCurrentWidget(w)

    def edit(self, obj):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'trabajosForm')
        w.setObjeto(obj)
        sw.setCurrentWidget(w)

    def delete(self, obj):
        with Session() as session:
            obj = session.merge(obj)
            reply = QMessageBox.question(self, "Advertencia", "Está a punto de eliminar un trabajo, si continúa no se podrá recuperar la información. ¿Desea continuar?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                session.delete(obj)
                session.commit()
                QMessageBox.information(self, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)

        self.search()
        
    def getDataTable(self, items: List['Trabajos'])-> Tuple:
        with Session() as session:
            headers = ["Cliente", "Trabajo","Fecha","Precio", "Pago", "Tono", "Técnica", "Opciones"]
            data = []
            dropdown_buttons = []
            
            for i in items:
                i = session.merge(i)
                fecha_trabajo = i.created_at.strftime('%d-%m-%Y')
                fecha_pago = f"{i.fecha_pago.strftime('%d-%m-%Y')} (Vía: {i.tipo_pago.tipo})" if i.fecha_pago else "Sin pagar"
                data.append([i.cliente.nombre_apellidos, i.tipo_trabajo.tipo, fecha_trabajo , i.price, fecha_pago, i.tonalidad.tono, i.tecnica.tecnica])
                dir = "views/images"
                size = QSize(30,30)
                edit = os.path.join(dir, 'edit-pencil.svg')
                trash = os.path.join(dir, 'trash.svg')
                buttons = [
                    {'Editar datos': self.edit, edit:size},
                    {'ELiminar': self.delete, trash:size},
                ]
                dropdown_buttons.append(buttons)
                
        return headers, data, dropdown_buttons, items