import typing
from PyQt6.QtCore import QLocale, QDate
from PyQt6.QtWidgets import QWidget, QMessageBox
from config import Session
from models import TipoTrabajos, Trabajos
from utils import REFRESH
from views.RangoStats_ui import Ui_StatsPerRango

class RangoStats(QWidget, Ui_StatsPerRango):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_refresh.setIcon(REFRESH)
        locale = QLocale(QLocale.Language.Spanish)
        cfecha = QDate.currentDate()
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
        self.totalTrabajos = 0
        self.totalCash = 0
        for anio in range(2000, cfecha.year()+1):
            self.cb_anio_inicio.addItem(str(anio), anio)
            self.cb_anio_fin.addItem(str(anio), anio)
        self.cb_anio_inicio.setCurrentIndex(self.cb_anio_inicio.findData(cfecha.year()))
        self.cb_anio_fin.setCurrentIndex(self.cb_anio_fin.findData(cfecha.year()))

        for mes in range(1, 13):
            nombre_mes = locale.monthName(mes)
            self.cb_mes_inicio.addItem(nombre_mes.capitalize(), mes)
            self.cb_mes_fin.addItem(nombre_mes.capitalize(), mes)
        self.cb_mes_inicio.setCurrentIndex(self.cb_mes_inicio.findData(cfecha.month()))
        self.cb_mes_fin.setCurrentIndex(self.cb_mes_fin.findData(cfecha.month()))
        
        self.actualizar_dias_mes(self.cb_dia_inicio, cfecha.month(), cfecha.year())
        self.cb_mes_inicio.currentIndexChanged.connect(self.actualizar_dias_w)
        self.cb_anio_inicio.currentIndexChanged.connect(self.actualizar_dias_w)
        self.cb_dia_inicio.setCurrentIndex(self.cb_dia_inicio.findData(cfecha.day()))

        self.actualizar_dias_mes(self.cb_dia_fin, cfecha.month(), cfecha.year())
        self.cb_mes_fin.currentIndexChanged.connect(self.actualizar_dias_f)
        self.cb_anio_fin.currentIndexChanged.connect(self.actualizar_dias_f)
        self.cb_dia_fin.setCurrentIndex(self.cb_dia_fin.findData(cfecha.day()))
        self.bt_refresh.clicked.connect(self.change_data)
    
    def fecha_inicial(self):
        d = self.cb_dia_inicio.currentData()
        m = self.cb_mes_inicio.currentData()
        y = self.cb_anio_inicio.currentData()
        return QDate(y,m,d)

    def fecha_final(self):
        d = self.cb_dia_fin.currentData()
        m = self.cb_mes_fin.currentData()
        y = self.cb_anio_fin.currentData()
        return QDate(y,m,d)
    
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
        self.actualizar_dias_mes(self.cb_dia_inicio, self.cb_mes_inicio.currentData(), self.cb_anio_inicio.currentData())

    def actualizar_dias_f(self):
        self.actualizar_dias_mes(self.cb_dia_fin, self.cb_mes_fin.currentData(), self.cb_anio_fin.currentData())

    def showEvent(self, a0) -> None:
        self.loadTrabajos()
        self.loadData()
        return super().showEvent(a0)

    def change_data(self):
        trabajos = self.trabajosDiarios()
        if trabajos != False:    
            self.totalTrabajos = len(trabajos)
            self.totalCash = sum(trabajo.price for trabajo in trabajos)
            self.t_trabajos.setText(str(self.totalTrabajos))
            self.t_cash.setText(str(self.totalCash))

    def loadData(self):
        self.fecha = QDate.currentDate()
        self.fecha_fin = QDate.currentDate()
        self.cb_anio_inicio.setCurrentIndex(self.cb_anio_inicio.findData(self.fecha.year()))
        self.cb_mes_inicio.setCurrentIndex(self.cb_mes_inicio.findData(self.fecha.month()))
        self.cb_dia_inicio.setCurrentIndex(self.cb_dia_inicio.findData(self.fecha.day()))
        self.cb_anio_fin.setCurrentIndex(self.cb_anio_fin.findData(self.fecha_fin.year()))
        self.cb_mes_fin.setCurrentIndex(self.cb_mes_fin.findData(self.fecha_fin.month()))
        self.cb_dia_fin.setCurrentIndex(self.cb_dia_fin.findData(self.fecha_fin.day()))
        self.change_data()
        
    def trabajosDiarios(self):
        fecha = self.fecha_inicial().toPyDate()
        fecha_fin = self.fecha_final().toPyDate()
        trabajo = self.cb_trabajos.currentData()
        if fecha > fecha_fin:
            QMessageBox.critical(self.mainWindowWidget,"Error", "La fecha final no puede ser menor que la fecha de inicio. Rectifique los datos")
            self.t_trabajos.setText(str(0))
            self.t_cash.setText(str(0))
            return False
        with Session() as session:
            q = session.query(Trabajos)
            if trabajo != None:
                q = q.filter(Trabajos.tipo_trabajo_id == trabajo)
            w = q.all()
        q = list(filter(lambda x: x.created_at.date() >= fecha and x.created_at.date() <= fecha_fin, w))
        return q

    def loadTrabajos(self):
        self.cb_trabajos.clear()
        self.cb_trabajos.setPlaceholderText("Todos")
        with Session() as session:
            self.cb_trabajos.addItem("Todos", None)
            q = session.query(TipoTrabajos).all()
            for i in q:
                self.cb_trabajos.addItem(i.tipo, i.id)
            self.cb_trabajos.setCurrentIndex(-1)

    def changeTrabajos(self):
        self.change_data()