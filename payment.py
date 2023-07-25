import typing
from PyQt6 import QtCore
from config import Session
from models import TipoTrabajos, Trabajos
from views.viaPagosForm_ui import Ui_viaPagosForm
from PyQt6.QtWidgets import QDialog, QComboBox, QMessageBox
from PyQt6.QtCore import QDate, QLocale

class Payment(QDialog, Ui_viaPagosForm):
    def __init__(self, trabajo: Trabajos, parent = None, mainwindow=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.trabajo = trabajo
        self.mainwindow = mainwindow
        self.bt_cancel.clicked.connect(self.cancel)
        locale = QLocale(QLocale.Language.Spanish)
        self.loadCB()
        self.search_via.textChanged.connect(self.s_tipo)
        fecha = QDate.currentDate()
        self.fecha_actual = fecha
        for anio in range(2000, fecha.year()+1):
            self.cb_anno.addItem(str(anio), anio)
        self.cb_anno.setCurrentIndex(self.cb_anno.findData(fecha.year()))

        for mes in range(1, 13):
            nombre_mes = locale.monthName(mes)
            self.cb_mes.addItem(nombre_mes.capitalize(), mes)
        self.cb_mes.setCurrentIndex(self.cb_mes.findData(fecha.month()))

        self.actualizar_dias_mes(self.cb_dia, fecha.month(), fecha.year())
        self.cb_dia.setCurrentIndex(self.cb_dia.findData(fecha.day()))
        self.cb_mes.currentIndexChanged.connect(self.actualizar_dias_w)

        self.bt_save.clicked.connect(self.save)

        self.loadData()
        self.setStyleSheet("""
        QFrame{
            background-color: rgb(54,72,100);
        }
        """)

    def loadData(self):
        with Session() as session:
            self.trabajo = session.merge(self.trabajo)
            if self.trabajo.tipo_pago_id is not None:
                fecha = QDate(self.trabajo.fecha_pago.year, self.trabajo.fecha_pago.month, self.trabajo.fecha_pago.day)
                self.cb_via.setCurrentIndex(self.cb_via.findData(self.trabajo.tipo_pago_id))
                self.cb_anno.setCurrentIndex(self.cb_anno.findData(fecha.year()))
                self.cb_mes.setCurrentIndex(self.cb_mes.findData(fecha.month()))
                self.cb_dia.setCurrentIndex(self.cb_dia.findData(fecha.day()))

    def s_tipo(self):
        text = self.search_via.text()
        ph = "Seleccione"
        self.cb_via.clear()
        if text != "":
            with Session() as session:
                q = session.query(TipoTrabajos).filter(TipoTrabajos.tipo.like(f"%{text}%")).all()
                if not len(q):
                    ph = "Sin resultados"
                for item in q:
                    self.cb_via.addItem(item.tipo, item.id)
            self.cb_via.setPlaceholderText(ph)
        else:
            self.loadCB()

    def loadCB(self):
        ph = "Seleccione"
        self.cb_via.clear()
        with Session() as session:
            q = session.query(TipoTrabajos).all()
            for item in q:
                self.cb_via.addItem(item.tipo, item.id)
            self.cb_via.setPlaceholderText(ph)

    def cancel(self):
        return self.reject()

    def actualizar_dias_mes(self, cb_day: QComboBox, month: int, year: int):
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
        self.actualizar_dias_mes(self.cb_dia, self.cb_mes.currentData(), self.cb_anno.currentData())

    def save(self):
        fecha = QDate(self.cb_anno.currentData(), self.cb_mes.currentData(), self.cb_dia.currentData())
        if self.cb_via.currentIndex() != -1:
            via = self.cb_via.currentData()
            with Session() as session:
                self.trabajo = session.merge(self.trabajo)
                self.trabajo.tipo_pago_id = via
                self.trabajo.fecha_pago = fecha.toPyDate()
                session.add(self.trabajo)
                session.commit()
        else:
           QMessageBox.critical(self.mainwindow, "Error", "Debe seleccionar un \"modo de pago\" antes de proceder a realizar el pago del trabajo", QMessageBox.StandardButton.Ok)
           return
        return self.accept()