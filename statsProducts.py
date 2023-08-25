from functools import reduce
import typing
from PyQt6 import QtGui
from PyQt6.QtCore import QDate, QLocale
from PyQt6.QtWidgets import QWidget
from sqlalchemy import Date, cast, func
from config import Session
from models import Io_productos, Productos
from views.statsProductsDiaries_ui import Ui_StatsProductsDay

class StatsProd(QWidget, Ui_StatsProductsDay):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)
        locale = QLocale(QLocale.Language.Spanish)
        cfecha = QDate.currentDate()
        self.compras = 0
        self.ventas = 0
        with Session() as session:
            productos = session.query(Productos).all()
        
        for p in productos:
            self.cb_producto.addItem(p.nick, p.id)
        self.cb_producto.setCurrentIndex(0)

        for anio in range(2000, cfecha.year()+1):
            self.cb_anio.addItem(str(anio), anio)
        self.cb_anio.setCurrentIndex(self.cb_anio.findData(cfecha.year()))

        for mes in range(1, 13):
            nombre_mes = locale.monthName(mes)
            self.cb_mes.addItem(nombre_mes.capitalize(), mes)
        self.cb_mes.setCurrentIndex(self.cb_mes.findData(cfecha.month()))
        
        self.actualizar_dias_mes(self.cb_dia, cfecha.month(), cfecha.year())
        self.cb_mes.currentIndexChanged.connect(self.actualizar_dias_w)
        self.cb_dia.currentIndexChanged.connect(self.updateFecha)
        self.cb_anio.currentIndexChanged.connect(self.actualizar_dias_w)
        self.cb_dia.setCurrentIndex(self.cb_dia.findData(cfecha.day()))
        self.cb_producto.currentIndexChanged.connect(self.change_data)

    @property
    def fecha(self):
        return self._fecha
    
    @fecha.setter
    def fecha(self, value):
        self._fecha = value
        self.change_data()

    @fecha.getter
    def fecha(self):
        return self._fecha

    def prod(self)->Productos:
        identifier = self.cb_producto.currentData()
        if identifier != None:
            with Session() as session:
                p = session.query(Productos).get(identifier)
        else:
            p = None
        return p
    
    def actualizar_dias_mes(self, cb_day, month: int, year: int):
        days = QDate.daysInMonth(QDate(year, month, 1))
        data = cb_day.currentData()
        cb_day.clear()
        for i in range(1,days+1):
            cb_day.addItem(str(i),i)
        
        if data:
            if data < days+1:
                cb_day.setCurrentIndex(cb_day.findData(data))
            else:
                cb_day.setCurrentIndex(-1)

    def actualizar_dias_w(self):
        self.actualizar_dias_mes(self.cb_dia, self.cb_mes.currentData(), self.cb_anio.currentData())
        self.fecha = QDate(self.cb_anio.currentData(),self.cb_mes.currentData(), self.cb_dia.currentData())

    def showEvent(self, a0) -> None:
        self.loadData()
        return super().showEvent(a0)

    def change_data(self):
        p = self.productosDiarios()
        if p != None:
            self.compras = sum(producto.cant for producto in p[0])
            self.ventas = sum(producto.cant for producto in p[1])
        else:
            self.compras = 0
            self.ventas = 0
        self.lb_comprados.setText(str(self.compras))
        self.lb_vendidos.setText(str(self.ventas))

    def loadData(self):
        self.fecha = QDate.currentDate()
        self.cb_producto.clear()
        with Session() as session:
            p = session.query(Productos).all()
        for i in p:
            self.cb_producto.addItem(i.nick, i.id)
        self.cb_producto.setCurrentIndex(0)
        self.cb_anio.setCurrentIndex(self.cb_anio.findData(self._fecha.year()))
        self.cb_mes.setCurrentIndex(self.cb_mes.findData(self._fecha.month()))
        self.cb_dia.setCurrentIndex(self.cb_dia.findData(self._fecha.day()))

    def updateFecha(self):
        self.fecha = QDate(self.cb_anio.currentData(),self.cb_mes.currentData(), self.cb_dia.currentData())

    def productosDiarios(self):
        fecha = self.fecha.toPyDate()
        p = self.prod()
        if p != None:
            with Session() as session:
                p = session.merge(p)
                entrantes = list(filter(lambda x: x.fecha == fecha and x.io == "in", p.io_productos))
                salientes = list(filter(lambda x: x.fecha == fecha and x.io == "out", p.io_productos))
            q = [entrantes, salientes]
        else:
            q = None
            
        return q
