from typing import List, Tuple
from config import Session
from payment import Payment
from strippedTable import StripedTable
from utils import BACK_ARROW, ICON_SAVE, INVERT, PLUS, REFRESH, TIPOS_TRABAJOS, eliminar_contenido
from views.trabajosIndex_ui import Ui_trabajosIndex
from views.trabajoForm_ui import Ui_trabajoForm
from PyQt6.QtWidgets import QWidget, QMessageBox, QComboBox
from PyQt6.QtCore import QSize, QDate, QLocale, QDateTime, QTime
from PyQt6.QtGui import QDoubleValidator
from models import Trabajos, Clients, TipoTrabajos, Tonalidades, Tecnicas
import os, re
from sqlalchemy import or_


class TrabajosIndex(QWidget, Ui_trabajosIndex):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.Desc = False
        self.table = None
        """ self.fecha_actual = QDate.currentDate() """
        self.bt_tipos.clicked.connect(self.tipos_index)
        self.le_search.textChanged.connect(self.search)
        self.bt_create.clicked.connect(self.create)
        self.bt_create.setIcon(PLUS)
        self.bt_tipos.setIcon(TIPOS_TRABAJOS)
        self.bt_revertir.setIcon(INVERT)
        self.bt_revertir.clicked.connect(self.invert)
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

    def invert(self):
        self.Desc = not self.Desc
        self.setItemsTable()

    def tipos_index(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'tiposTrabajosIndex')
        w.search()
        sw.setCurrentWidget(w)

    def search(self):
        self.setItemsTable()
    
    def showEvent(self, a0) -> None:
        self.setItemsTable()
        return super().showEvent(a0)
    
    def setItemsTable(self):
            headers, data, dropdown_buttons, objects = self.getDataTable(self.Works())
            eliminar_contenido(self.layout_tabla)
            self.table = StripedTable(headers, data, dropdown_buttons, objects, Desc=self.Desc)
            self.layout_tabla.addWidget(self.table)
            
    def Works(self):
        le = self.le_search.text()
        today = QDate.currentDate().toPyDate()
        with Session() as session:
            q = session.query(Trabajos)
            if le != "":
                if le.isdigit():
                    q = session.query(Trabajos).filter(Trabajos.price.like(f"%{le}%"))
                else:
                    q = session.query(Trabajos).select_from(Trabajos).join(Clients).join(TipoTrabajos).filter(or_(Clients.nombre_apellidos.like(f"%{le}%"), TipoTrabajos.tipo.like(f"%{le}%")))
            q = q.all()
            q = list(filter(lambda x: x.created_at.date() == today, q))
            
        return q

    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'trabajoForm')
        w.refresh()
        w.load_cb()
        sw.setCurrentWidget(w)

    def payWork(self, obj: Trabajos):
        payment =  Payment(obj, self, self.mainWindowWidget)
        payment.exec()
    

    def edit(self, obj):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'trabajoForm')
        w.load_cb()
        w.setObjeto(obj)
        sw.setCurrentWidget(w)

    def delete(self, obj):
        with Session() as session:
            obj = session.merge(obj)
            reply = QMessageBox.question(self.mainWindowWidget, "Advertencia", "Está a punto de eliminar un trabajo, si continúa no se podrá recuperar la información. ¿Desea continuar?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                session.delete(obj)
                session.commit()
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)

        self.search()
    
    def getDataTable(self, items: List['Trabajos'])-> Tuple:
        with Session() as session:
            headers = ["Cliente", "Trabajo","Fecha","Precio", "Pago", "Tono", "Técnica", "Opciones"]
            data = []
            dropdown_buttons = []
            
            for i in items:
                i = session.merge(i)
                fecha_trabajo = i.created_at.strftime('%d-%m-%Y')
                fecha_pago = f"{i.fecha_pago.strftime('%d-%m-%Y')} (Vía: {i.tipo_pago.tipo})" if i.tipo_pago_id is not None else "Sin pagar"
                tono = f"{i.tonalidad.tono}" if i.tonalidad_id is not None else "--"
                tecnica = f"{i.tecnica.tecnica}" if i.tecnica_id is not None else "--"
                data.append([i.cliente.nombre_apellidos, i.tipo_trabajo.tipo, fecha_trabajo , str(i.price), fecha_pago, tono, tecnica])
                dir = "views/images"
                size = QSize(30,30)
                edit = os.path.join(dir, 'edit-pencil.svg')
                trash = os.path.join(dir, 'trash.svg')
                pay = os.path.join(dir, 'credit-card.svg')
                buttons = [
                    {'Editar datos': self.edit, edit:size},
                    {'Pago': self.payWork, pay:size},
                    {'ELiminar': self.delete, trash:size},
                ]
                dropdown_buttons.append(buttons)
                
        return headers, data, dropdown_buttons, items
    

class TrabajoForm(QWidget,Ui_trabajoForm):

        def __init__(self,parent: QWidget | None = ..., **kwargs) -> None:
            super().__init__(parent)
            locale = QLocale(QLocale.Language.Spanish)
            self.setupUi(self)
            self.bt_back.setIcon(BACK_ARROW)
            self.bt_save.setIcon(ICON_SAVE)
            self.bt_refresh.setIcon(REFRESH)
            fecha = QDate.currentDate()
            self.fecha_actual = fecha
            self.bt_save.clicked.connect(self.save)
            self.obj = None
            self.bt_back.clicked.connect(self.mostrar_widget)
            self.cb_client.setPlaceholderText("Sin Resultados")
            self.cb_t_trabajo.setPlaceholderText("Seleccione")
            self.cb_tecnica.setPlaceholderText("Sin Resultados")
            self.cb_tono.setPlaceholderText("Sin Resultados")
            self.search_client.textChanged.connect(self.s_client)
            self.search_tecnica.textChanged.connect(self.s_tecnica)
            self.search_tono.textChanged.connect(self.s_tono)
            self.precio.setValidator(QDoubleValidator())
            self.precio.textChanged.connect(self.validate_precio)
            self.bt_refresh.clicked.connect(self.refresh)
           

            for anio in range(2000, fecha.year()+1):
                self.w_year.addItem(str(anio), anio)
            self.w_year.setCurrentIndex(self.w_year.findData(fecha.year()))

            for mes in range(1, 13):
                nombre_mes = locale.monthName(mes)
                self.w_month.addItem(nombre_mes.capitalize(), mes)
            self.w_month.setCurrentIndex(self.w_month.findData(fecha.month()))

            self.actualizar_dias_mes(self.w_day, fecha.month(), fecha.year())
            self.w_day.setCurrentIndex(self.w_day.findData(fecha.day()))
            self.w_month.currentIndexChanged.connect(self.actualizar_dias_w)
            self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
            
        def load_cb(self):
            self.cb_t_trabajo.clear()
            self.cb_t_trabajo.setCurrentIndex(-1)
            with Session() as session:
               trabajos = session.query(TipoTrabajos).all()

            for w in trabajos:
               self.cb_t_trabajo.addItem(w.tipo, w.id)


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
            self.actualizar_dias_mes(self.w_day, self.w_month.currentData(), self.w_year.currentData())


        def s_client(self):
            t = self.search_client.text()
            with Session() as session:
                self.cb_client.clear()
                if t == "":
                    self.cb_client.setPlaceholderText("Sin Resultados")
                else:
                    q = session.query(Clients).filter(Clients.nombre_apellidos.like(f"%{t}%")).all()
                    if len(q) > 0:
                        self.cb_client.setPlaceholderText("Seleccione")
                        for item in q:
                            self.cb_client.addItem(item.nombre_apellidos, item.id)
                    else:
                        self.cb_client.setPlaceholderText("Sin Resultados")

        def s_tecnica(self):
            t = self.search_tecnica.text()
            with Session() as session:
                self.cb_tecnica.clear()
                if t == "":
                    self.cb_tecnica.setPlaceholderText("Sin Resultados")
                else:
                    q = session.query(Tecnicas).filter(Tecnicas.tecnica.like(f"%{t}%")).all()
                    if len(q) > 0:
                        self.cb_tecnica.setPlaceholderText("Seleccione")
                        for item in q:
                            self.cb_tecnica.addItem(item.tecnica, item.id)
                    else:
                        self.cb_tecnica.setPlaceholderText("Sin Resultados")

        def s_tono(self):
            t = self.search_tono.text()
            with Session() as session:
                self.cb_tono.clear()
                if t == "":
                    self.cb_tono.setPlaceholderText("Sin Resultados")
                else:
                    q = session.query(Tonalidades).filter(Tonalidades.tono.like(f"%{t}%")).all()
                    if len(q) > 0:
                        self.cb_tono.setPlaceholderText("Seleccione")
                        for item in q:
                            self.cb_tono.addItem(item.tono, item.id)
                    else:
                        self.cb_tono.setPlaceholderText("Sin Resultados")

        def validate_precio(self, text):
            regex = re.compile(r"^(\d*\.?\d*)$")
            match = regex.search(text)
            if not match:
                self.precio.setText(text[:-1])

        def save(self):
            cliente_id = self.cb_client.currentData()
            trabajo_id = self.cb_t_trabajo.currentData()
            tono_id = self.cb_tono.currentData()
            tecnica_id = self.cb_tecnica.currentData()
            precio =  self.precio.text()
            w_day = self.w_day.currentData()
            w_month = self.w_month.currentData()
            w_year = self.w_year.currentData()
            fecha_w = QDateTime(QDate(w_year,w_month, w_day), QTime()).toPyDateTime()

            if not cliente_id or not trabajo_id or precio == "":
                QMessageBox.warning(self.mainWindowWidget, "Advertencia", "Para llevar a cabo la acción debe llenar los campos correctamente", QMessageBox.StandardButton.Ok)
                return 
            
            with  Session() as session:
                if self.obj:
                    self.obj = session.merge(self.obj)
                    self.obj.cliente_id = cliente_id
                    self.obj.tipo_trabajo_id = trabajo_id
                    self.obj.tonalidad_id = tono_id
                    self.obj.tecnica_id = tecnica_id
                    self.obj.price = precio
                    self.obj.created_at = fecha_w
                else:
                    self.obj = Trabajos(cliente_id=cliente_id, tipo_trabajo_id=trabajo_id, tonalidad_id=tono_id, tecnica_id=tecnica_id, price=precio, created_at=fecha_w)

                session.add(self.obj)
                if self.obj.tipo_pago_id is not None:
                    titulo = "Datos del pago"
                    texto = "¿Desea editar datos del pago de este trabajo?"
                else:
                    titulo = "Realizar pago"
                    texto = "¿Desea ejecutar ahora el pago del trabajo?"
                """ try: """
                session.commit()
                reply = QMessageBox.question(self.mainWindowWidget, titulo, texto, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    payment = Payment(trabajo=self.obj,parent=self, mainwindow=self.mainWindowWidget)
                    payment.exec()
                self.mostrar_widget()
                self.refresh()
                self.obj = None
                QMessageBox.information(self.mainWindowWidget, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
                """ except:
                    QMessageBox.critical(self.mainWindowWidget, "Error", "Ha ocurrido un error. Comuníquese con el proveedor de su aplicación", QMessageBox.StandardButton.Ok) """
                
        def refresh(self):
            self.search_client.clear()
            self.search_tecnica.clear()
            self.search_tono.clear()
            self.cb_client.clear()
            self.cb_t_trabajo.setCurrentIndex(-1)
            self.cb_tecnica.setCurrentIndex(-1)
            self.cb_tono.setCurrentIndex(-1)
            self.precio.clear()
            fecha = QDate.currentDate()
            self.w_year.setCurrentIndex(self.w_year.findData(fecha.year()))
            self.w_month.setCurrentIndex(self.w_month.findData(fecha.month()))
            self.w_day.setCurrentIndex(self.w_day.findData(fecha.day()))


        def mostrar_widget(self):
            stackedWidget = self.parentWidget()
            w = stackedWidget.findChild(QWidget, "trabajosIndex")
            self.reload_data()
            stackedWidget.setCurrentWidget(w)
            self.bt_refresh.show()
            self.refresh()

        def reload_data(self):
            sw = self.parentWidget()
            w = sw.findChild(QWidget, "trabajosIndex")
            w.search()
            self.refresh()
            
        def setObjeto(self,obj: Trabajos):
            with Session() as session:
                self.obj = obj
                self.bt_refresh.hide()
                obj = session.merge(obj)
                self.setClient(obj.cliente)
                tec_id = -1
                ton_id = -1
                if obj.tecnica_id is not None:
                    tec = obj.tecnica.tecnica[:3]
                    tec_id =  obj.tecnica_id
                else:
                    tec = ""
                if obj.tonalidad_id is not None:
                    ton = obj.tonalidad.tono[:3]
                    ton_id =  obj.tonalidad_id
                else:
                    ton = ""
                self.search_tecnica.setText(tec)
                self.search_tono.setText(ton)
                self.cb_tecnica.setCurrentIndex(self.cb_tecnica.findData(tec_id))
                self.cb_tono.setCurrentIndex(self.cb_tono.findData(ton_id))
                self.cb_t_trabajo.setCurrentIndex(self.cb_t_trabajo.findData(obj.tipo_trabajo_id))
                self.precio.setText(str(obj.price))
                d = QDateTime(obj.created_at)
                self.w_year.setCurrentIndex(self.w_year.findData(d.date().year()))
                self.w_month.setCurrentIndex(self.w_month.findData(d.date().month()))
                self.w_day.setCurrentIndex(self.w_day.findData(d.date().day()))

        def setClient(self, client: Clients):
            n_ape = client.nombre_apellidos[:3]
            self.search_client.setText(n_ape)
            self.cb_client.setCurrentIndex(self.cb_client.findData(client.id))