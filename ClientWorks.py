import os
from typing import List, Tuple
from PyQt6 import QtGui
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QShowEvent

from payment import Payment
from views.clientWorks_ui import Ui_ClientWorks
from PyQt6.QtWidgets import QWidget, QStackedWidget
from config import DEFAULT_PICTURE, Session
from models import Clients, Trabajos
from strippedTable import StripedTable
from utils import BACK_ARROW, CHANGE_PAGE, default_image, file_exists


class ClientWorks(QWidget, Ui_ClientWorks):
    def __init__(self, client = None, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.table = None
        self.client = client
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
        self.bt_back.setIcon(BACK_ARROW)
        self.bt_change_page.setIcon(CHANGE_PAGE)
        self.bt_back.clicked.connect(self.back)
        self.bt_change_page.clicked.connect(self.change_page)

    def showEvent(self, a0: QShowEvent) -> None:
        self.setClient()
        return super().showEvent(a0)

    def setPic(self):
        ci = file_exists(self.client.ci, 'clients_pictures')
        if not ci:
            ci = DEFAULT_PICTURE
        default_image(self.lb_pic_works_client, ci, 'clients_pictures')

    def setClient(self):
        with Session() as session:
            self.client = session.merge(self.client)
            self.setPic()
            self.le_ci_client_works.setText(self.client.ci)
            self.le_full_name_client_works.setText(self.client.nombre_apellidos)
            self.le_gasto.setText(str(self.client.gastos()))
            headers, data, dropdowns_buttons, objects = self.getDataTable(self.client.trabajos)
            # Borrar la tabla existente y crear una nueva tabla con los nuevos datos
            if self.table is not None:
                self.verticalLayout_works.removeWidget(self.table)
                self.table.clearContents()
            self.table = StripedTable(headers, data, dropdowns_buttons, objects)
            self.verticalLayout_works.addWidget(self.table)
    
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
    
    def back(self):
        from ClientsList import ClientListWidget
        stacked: QStackedWidget = self.parentWidget()
        w = stacked.findChildren(ClientListWidget)
        for i in w:
            i.setParent(None)
        w = ClientListWidget(parent=stacked)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)

    def change_page(self):
        from showClient import ShowCLient
        stacked: QStackedWidget = self.parentWidget()
        w = stacked.findChildren(ShowCLient)
        for i in w:
            i.setParent(None)
        w = ShowCLient(parent=stacked, client=self.client)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)