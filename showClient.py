import os
from typing import List, Tuple
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QSize
from ClientsList import ClientListWidget
from config import DEFAULT_PICTURE, Session
from models import Clients, Socials, t_r_clients_socials, Trabajos
from payment import Payment
from strippedTable import StripedTable
from views.showClientView_ui import Ui_showClient
from PyQt6.QtWidgets import QWidget, QStackedWidget, QLabel, QLineEdit, QHBoxLayout
from PyQt6.QtGui import QFont
from utils import BACK_ARROW, CHANGE_PAGE, eliminar_contenido, file_exists, default_image

class ShowCLient(QWidget, Ui_showClient):
    def __init__(self, client: Clients = None, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.client = client
        self.bt_volver_show.setIcon(BACK_ARROW)
        self.bt_volver_show.clicked.connect(self.back)
        
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
        self.table = None
    
    def showEvent(self, a0) -> None:
        self.setClient()
        return super().showEvent(a0)
    
    def setPic(self):
        ci = file_exists(self.client.ci, 'clients_pictures')
        if not ci:
            ci = DEFAULT_PICTURE
        default_image(self.lb_pic_client_show_2, ci, 'clients_pictures')

    def setClient(self):
        with Session() as session:
            self.client = session.merge(self.client)
            self.setUserNamesSocials()
            self.setPersonalData()
            self.setWorks()
            

    def back(self):
        stacked: QStackedWidget = self.parentWidget()
        w = stacked.findChild(ClientListWidget)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)

    def change_page(self):
        from ClientWorks import ClientWorks
        stacked: QStackedWidget = self.parentWidget()
        w = stacked.findChildren(ClientWorks)
        for i in w:
            i.setParent(None)
        w = ClientWorks(parent=stacked, client=self.client)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)

    def setPersonalData(self):
        municipio = self.client.municipio_id
        pais = self.client.pais_id
        if municipio == None:
            self.le_municipio_show_2.setPlaceholderText("Sin municipio asignado")
            self.le_provincia_show_2.setPlaceholderText("Sin provinvia asignada")
        else:
            self.le_provincia_show_2.setText(self.client.municipio.provincia.provincia)
            self.le_municipio_show_2.setText(self.client.municipio.municipio)

        if pais == None:
            self.le_pais_show_2.setPlaceholderText("Sin país asignado")
        else:
            self.le_pais_show_2.setText(self.client.pais.pais)

        
        self.setPic()
        self.le_ci_show_2.setText(self.client.ci)
        self.le_phone_show_2.setText(self.client.phone)
        self.le_full_name_show_2.setText(self.client.nombre_apellidos)
        self.txted_notas_show_2.setText(self.client.notes)
        self.txted_alcance_show_2.setText(self.client.alcance)

    def setUserNamesSocials(self):
        tittle = QLabel("Redes Sociales ")
        tittle.setMinimumHeight(50)
        tittle.setFont(QFont("Times",50,20,True))
        tittle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        with Session() as session:
            socials = session.query(Socials).all()
            q = session.query(t_r_clients_socials).where(t_r_clients_socials.c.client_id == self.client.id).all()

            eliminar_contenido(self.layoutUsernames)
            self.layoutUsernames.addWidget(tittle)
            for i in q:
                s = list(filter(lambda x: x.id == i.social_id ,socials))
                s = s.pop()
                label = QLabel(self)
                label.setText(f"{s.social} :")
                line_edit = QLineEdit(self)
                line_edit.setText(str(i.username))
                socialName = str(s.social).replace(" ", "_")
                line_edit.setObjectName(f'le_{socialName}')
                hlayout = QHBoxLayout()
                hlayout.addWidget(label)
                hlayout.addWidget(line_edit)
                hlayout.setStretch(0,2)
                hlayout.setStretch(1,7)
                hlayout.setObjectName(f"layout_{socialName}")
                self.layoutUsernames.addLayout(hlayout)       

            
            

    def setWorks(self):
        self.gasto_total.setText(str(self.client.gastos()))
        
        with Session() as session:
            self.client = session.merge(self.client)
            headers, data, dropdowns_buttons, objects = self.getDataTable(self.client.trabajos)
                # Borrar la tabla existente y crear una nueva tabla con los nuevos datos
            if self.table is not None:
                self.layoutWorks.removeWidget(self.table)
                self.table.clearContents()
            self.table = StripedTable(headers, data, dropdowns_buttons, objects)
            self.table.setMinimumHeight(500)
            self.layoutWorks.addWidget(self.table)
    

    def getDataTable(self, trabajos: List['Trabajos'])-> Tuple:
        with Session() as session:
            headers = ["Trabajo", "Precio","Tipo de pago", "Fecha", "Opciones"]
            data = []
            dropdown_buttons = []
            for w in trabajos:
                w = session.merge(w)
                dir = "views/images"
                pay = os.path.join(dir, 'credit-card.svg')
                size = QSize(30,30)
                if w.tipo_pago_id is not None:
                    tipo_pago = w.tipo_pago.tipo
                else:
                    tipo_pago = "NO PAGADO"
                buttons = [{'Pago': self.payWork, pay:size}]
                dropdown_buttons.append(buttons)
                data.append([w.tipo_trabajo.tipo, str(w.price), tipo_pago, w.created_at.strftime('%d-%m-%Y')])
        return headers, data, dropdown_buttons, trabajos
    
    def payWork(self, obj: Trabajos):
        payment = Payment(obj, self, self.mainWindowWidget)
        payment.exec()