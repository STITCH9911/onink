from functools import reduce
import typing
from PyQt6 import QtGui
from PyQt6.QtCore import QDate, QLocale
from PyQt6.QtWidgets import QWidget
from sqlalchemy import Date, cast, func
from config import Session
from models import Trabajos
from views.statsPerDay_ui import Ui_StatsDay

class StatsDay(QWidget, Ui_StatsDay):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)
        locale = QLocale(QLocale.Language.Spanish)
        cfecha = QDate.currentDate()
        self.totalTrabajos = 0
        self.totalCash = 0
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
        trabajos = self.trabajosDiarios()
        self.totalTrabajos = len(trabajos)
        self.totalCash = sum(trabajo.price for trabajo in trabajos)
        self.t_trabajos.setText(str(self.totalTrabajos))
        self.t_cash.setText(str(self.totalCash))

    def loadData(self):
        self.fecha = QDate.currentDate()
        self.cb_anio.setCurrentIndex(self.cb_anio.findData(self._fecha.year()))
        self.cb_mes.setCurrentIndex(self.cb_mes.findData(self._fecha.month()))
        self.cb_dia.setCurrentIndex(self.cb_dia.findData(self._fecha.day()))

    def updateFecha(self):
        self.fecha = QDate(self.cb_anio.currentData(),self.cb_mes.currentData(), self.cb_dia.currentData())

    def trabajosDiarios(self):
        fecha = self.fecha.toPyDate()
        with Session() as session:
            w = session.query(Trabajos).all()
        
        q = list(filter(lambda x: x.created_at.date() == fecha, w))
        return q
