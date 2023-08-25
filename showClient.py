import typing
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from config import DEFAULT_PICTURE, Session
from models import Clients
from views.showClientView_ui import Ui_showClient
from PyQt6.QtWidgets import QWidget, QStackedWidget
from utils import BACK_ARROW, CHANGE_PAGE, file_exists, default_image

class ShowCLient(QWidget, Ui_showClient):
    def __init__(self, client: Clients = None, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.client = client
        self.bt_volver_show.setIcon(BACK_ARROW)
        self.bt_change_view_show.setIcon(CHANGE_PAGE)
        self.bt_volver_show.clicked.connect(self.back)
        self.bt_change_view_show.clicked.connect(self.change_page)
    
    
    def showEvent(self, a0) -> None:
        self.setClient()
        return super().showEvent(a0)
    
    def setPic(self):
        ci = file_exists(self.client.ci, 'clients_pictures')
        if not ci:
            ci = DEFAULT_PICTURE
        default_image(self.lb_pic_client_show, ci, 'clients_pictures')

    def setClient(self):
        with Session() as session:
            self.client = session.merge(self.client)
            municipio = self.client.municipio_id
            pais = self.client.pais_id
            if municipio == None:
                self.le_municipio_show.setPlaceholderText("Sin municipio asignado")
                self.le_provincia_show.setPlaceholderText("Sin provinvia asignada")
            else:
                self.le_provincia_show.setText(self.client.municipio.provincia.provincia)
                self.le_municipio_show.setText(self.client.municipio.municipio)

            if pais == None:
                self.le_pais_show.setPlaceholderText("Sin país asignado")
            else:
                self.le_pais_show.setText(self.client.pais.pais)

            
            self.setPic()
            self.le_ci_show.setText(self.client.ci)
            self.le_phone_show.setText(self.client.phone)
            self.le_full_name_show.setText(self.client.nombre_apellidos)
            self.txted_notas_show.setText(self.client.notes)
            self.txted_alcance_show.setText(self.client.alcance)

    def back(self):
        stacked: QStackedWidget = self.parentWidget()
        w = stacked.findChildren(QWidget, 'ClientsListWidget')
        for i in w:
            stacked.removeWidget(i)
        from ClientsList import ClientListWidget
        w = ClientListWidget(parent=stacked)
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