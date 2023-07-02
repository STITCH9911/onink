from typing import List, Tuple
from PyQt6 import QtCore
from views.clientWorks_ui import Ui_ClientWorks
from PyQt6.QtWidgets import QWidget
from config import DEFAULT_PICTURE, Session

from models import Clients, Trabajos
from strippedTable import StripedTable
from utils import default_image, file_exists


class ClientWorks(QWidget, Ui_ClientWorks):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.table = None
    
    def setPic(self):
        ci = file_exists(self.client.ci, 'clients_pictures')
        if not ci:
            ci = DEFAULT_PICTURE
        default_image(self.lb_pic_works_client, ci, 'clients_pictures')


    def setClient(self, client: Clients):
        with Session() as session:
            self.client = session.merge(client)
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
            headers = ["Trabajo", "Precio","Tipo de pago", "Fecha"]
            data = []
            dropdown_buttons = []
            for w in trabajos:
                w = session.merge(w)
                data.append([w.tipo_trabajo.tipo, w.price, w.tipo_pago.tipo, w.created_at.strftime('%d-%m-%Y')])
        return headers, data, dropdown_buttons, trabajos
    
    def setFunciones(self, funcVolver, funcChangePage):
        self.bt_back.clicked.connect(funcVolver)
        self.bt_change_page.clicked.connect(funcChangePage)