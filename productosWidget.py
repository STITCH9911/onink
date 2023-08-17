import re
from typing import List, Tuple
from sqlalchemy.exc import IntegrityError
from config import Session
from models import Productos
from strippedTable import StripedTable
from utils import BACK_ARROW, ICON_SAVE, PLUS, PRODUCTOS_WHITE
from views.productsIndex_ui import Ui_ProductosIndex
from views.productsForm_ui import Ui_ProductosForm
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QSize
import os
from inventarioDialog import IO_Products

class ProductosIndex(QWidget, Ui_ProductosIndex):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.le_search.textChanged.connect(self.search)
        self.table = None
        self.bt_add.clicked.connect(self.create)
        self.bt_add.setIcon(PLUS)
        self.search()
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

    def editFunc(self,obj):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'ProductosForm')
        w.setObjeto(obj)
        sw.setCurrentWidget(w)
    
    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "ProductosForm")
        sw.setCurrentWidget(w)
    
    def setItemsTable(self, objects):
        headers, data, dropdown_buttons, objects = self.getDataTable(objects)
        if self.table is not None:
            self.tablaLayout.removeWidget(self.table)
            self.table.clearContents()        
        self.table = StripedTable(headers, data, dropdown_buttons, objects)
        self.tablaLayout.addWidget(self.table)

    def search(self):
        le = self.le_search.text()
        with Session() as session:
            if le != "":
                items = session.query(Productos).filter(Productos.nick.like(f"%{le}%")).all()
            else:
                items = session.query(Productos).all()
        self.setItemsTable(items)

    def getDataTable(self, items: List['Productos'])-> Tuple:
        with Session() as session:
            headers = ["Productos", "Existencias", "Opciones"]
            data = []
            dropdown_buttons = []
            
            for i in items:
                i = session.merge(i)
                data.append([i.nick, str(i.existencia)])
                dir = "views/images"
                size = QSize(30,30)
                edit = os.path.join(dir, 'edit-pencil.svg')
                trash = os.path.join(dir, 'trash.svg')
                pack_plus = os.path.join(dir, 'package-plus.svg')
                pack_minus = os.path.join(dir, 'package-minus.svg')
                buttons = [
                    {'Editar datos': self.editFunc, edit:size},
                    {'Agregar a inventario': self.put_in, pack_plus:size},
                    {'Eliminar de inventario': self.put_out, pack_minus:size},
                    {'ELiminar': self.delete, trash:size},
                ]
                dropdown_buttons.append(buttons)
                
        return headers, data, dropdown_buttons, items
    
    def delete(self, obj):
        with Session() as session:
            obj = session.merge(obj)
            reply = QMessageBox.question( self.mainWindowWidget, "Advertencia", "Está a punto de eliminar un producto, si continúa no se podrá recuperar la información. ¿Desea continuar?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                session.delete(obj)
                session.commit()
                QMessageBox.information( self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)

        self.search()
        
    def put_in(self, obj: Productos):
        io = IO_Products(self.mainWindowWidget,obj,"in",self)
        io.exec()
        self.search()
    
    def put_out(self,obj: Productos):
        io = IO_Products(self.mainWindowWidget,obj,"out",self)
        io.exec()
        self.search()


class ProductosForm(QWidget,Ui_ProductosForm):

    def __init__(self,parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_save.clicked.connect(self.save)
        self.bt_save.setIcon(ICON_SAVE)
        self.bt_back.setIcon(BACK_ARROW)
        self.pushButton_2.setIcon(PRODUCTOS_WHITE)
        self.obj = None
        self.bt_back.clicked.connect(self.mostrar_widget)
        self.le_producto.returnPressed.connect(self.save)
        self.le_price.returnPressed.connect(self.save)
        self.le_price.textChanged.connect(self.validate_precio)
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

    def save(self):
        if self.le_producto.text() == "" or self.le_price.text() == "":
            QMessageBox.warning( self.mainWindowWidget, "Advertencia", "Para llevar a cabo la acción debe llenar los campos correctamente", QMessageBox.StandardButton.Ok)
            return 

        with  Session() as session:
            if self.obj:
                self.obj = session.merge(self.obj)
                self.obj.producto = self.le_producto.text()
                self.obj.price = float(self.le_price.text())
                self.obj.nick = f"{self.le_producto.text()} ( {self.le_price.text()} )"
                session.add(self.obj)
            else:
                nick = f"{self.le_producto.text()} ( {float(self.le_price.text())} )"
                obj = Productos(producto=self.le_producto.text(), existencia=0, nick=nick, price=float(self.le_price.text()))
                session.add(obj)       
            try:
                session.commit()
                self.mostrar_widget()
                self.le_producto.clear()
                self.le_price.clear()
                self.obj = None
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
            except IntegrityError:
                QMessageBox.critical( self.mainWindowWidget, "Error", "Ya existe este producto.", QMessageBox.StandardButton.Ok)
            
    def validate_precio(self, text):
        regex = re.compile(r"^(\d*\.?\d*)$")
        match = regex.search(text)
        if not match:
            self.le_price.setText(text[:-1])

    def mostrar_widget(self):
        stackedWidget = self.parentWidget()
        w = stackedWidget.findChild(QWidget, "ProductosIndex")
        self.reload_data()
        stackedWidget.setCurrentWidget(w)
        self.le_producto.clear()
        self.le_price.clear()

    def reload_data(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, "ProductosIndex")
        w.search()
        self.le_producto.clear()
        self.le_price.clear()
        
    def setObjeto(self,obj):
        self.obj = obj
        self.le_producto.setText(obj.producto)
        self.le_price.setText(str(obj.price))