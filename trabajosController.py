from typing import List, Tuple
from config import Session
from strippedTable import StripedTable
from views.trabajosIndex_ui import Ui_trabajosIndex
from views.trabajoForm_ui import Ui_trabajoForm
from PyQt6.QtWidgets import QWidget, QMessageBox, QComboBox
from PyQt6.QtCore import QSize, QDate, QLocale
from PyQt6.QtGui import QDoubleValidator
from models import Trabajos, Clients, TipoTrabajos, TiposPagos, Tonalidades, Tecnicas
import os, re
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError


class TrabajosIndex(QWidget, Ui_trabajosIndex):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.table = None
        self.fecha_actual = QDate.currentDate()
        self.bt_tipos.clicked.connect(self.tipos_index)
        self.le_search.textChanged.connect(self.search)
        self.bt_create.clicked.connect(self.create)
        """self.l_fechaW = QLabel()
        self.l_fechaW.setText("Fecha de trabajo: ")
        self.l_fechaP = QLabel()
        self.l_fechaP.setText("Fecha de pago: ")
         self.date_w = NullableDateEdit()
        self.date_p = NullableDateEdit()
        self.date_p.setDate(QDate(0,0,0))
        self.filterDatesLayout.addWidget(self.l_fechaW, 1)
        self.filterDatesLayout.addWidget(self.date_w, 4)
        self.filterDatesLayout.addWidget(self.l_fechaP, 1)
        self.filterDatesLayout.addWidget(self.date_p, 4) """
        self.search()

    def tipos_index(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'tiposTrabajosIndex')
        w.search()
        sw.setCurrentWidget(w)

    def setItemsTable(self, objects):
            headers, data, dropdown_buttons, objects = self.getDataTable(objects)
            if self.table is not None:
                self.layout_tabla.removeWidget(self.table)
                self.table.clearContents()        
            self.table = StripedTable(headers, data, dropdown_buttons, objects)
            self.layout_tabla.addWidget(self.table)
            
    def search(self):
        le = self.le_search.text()
        with Session() as session:
            q = session.query(Trabajos).select_from(Trabajos).join(Clients).join(TipoTrabajos).join(TiposPagos).join(Tonalidades).join(Tecnicas)
            if le != "":
                if le.isdigit():
                    q = q.filter(Trabajos.price.like(f"%{le}%"))
                else:
                    q = q.where(or_(Clients.nombre_apellidos.like(f"%{le}%"),TipoTrabajos.tipo.like(f"%{le}%"),TiposPagos.tipo.like(f"%{le}%"),Tonalidades.tono.like(f"%{le}%"),Tecnicas.tecnica.like(f"%{le}%")))
            q = q.all()
        self.setItemsTable(q)

    def create(self):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'trabajoForm')
        sw.setCurrentWidget(w)

    def edit(self, obj):
        sw = self.parentWidget()
        w = sw.findChild(QWidget, 'trabajoForm')
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
                data.append([i.cliente.nombre_apellidos, i.tipo_trabajo.tipo, fecha_trabajo , str(i.price), fecha_pago, i.tonalidad.tono, i.tecnica.tecnica])
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
    

class TrabajoForm(QWidget,Ui_trabajoForm):

        def __init__(self,parent: QWidget | None = ..., **kwargs) -> None:
            super().__init__(parent)
            locale = QLocale(QLocale.Language.Spanish)
            self.setupUi(self)
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
            with Session() as session:
                trabajos = session.query(TipoTrabajos).all()

            for w in trabajos:
                self.cb_t_trabajo.addItem(w.tipo, w.id)

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
            fecha_w = QDate(w_year,w_month, w_day)

            if not cliente_id or not trabajo_id or precio == "":
                QMessageBox.warning(self.parentWidget(), "Advertencia", "Para llevar a cabo la acción debe llenar los campos correctamente", QMessageBox.StandardButton.Ok)
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
                    session.add(self.obj)
                else:
                    obj = Trabajos(cliente_id=cliente_id, tipo_trabajo_id=trabajo_id, tonalidad_id=tono_id, tecnica_id=tecnica_id, price=precio, created_at=fecha_w.toPyDate())
                    session.add(obj)
                                
                try:
                    session.commit()
                    self.mostrar_widget()
                    self.refresh()
                    self.obj = None
                    QMessageBox.information(self, "Correcto", "Operación completada correctamente", QMessageBox.StandardButton.Ok)
                except IntegrityError:
                    QMessageBox.critical(self, "Error", "Ya existe este tipo de pago.", QMessageBox.StandardButton.Ok)
                
        def refresh(self):
            self.cb_client.clear()
            self.cb_t_trabajo.clear()
            self.cb_tecnica.clear()
            self.cb_tono.clear()


        def mostrar_widget(self):
            stackedWidget = self.parentWidget()
            w = stackedWidget.findChild(QWidget, "tecnicaIndex")
            self.reload_data()
            stackedWidget.setCurrentWidget(w)
            self.lineEdit.clear()

        def reload_data(self):
            sw = self.parentWidget()
            w = sw.findChild(QWidget, "tecnicaIndex")
            w.search()
            self.lineEdit.clear()
            
        def setObjeto(self,obj):
            self.obj = obj
            self.lineEdit.setText(obj.tecnica)