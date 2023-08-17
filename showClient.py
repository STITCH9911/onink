import typing
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from config import DEFAULT_PICTURE, Session
from models import Clients
from views.showClientView_ui import Ui_showClient
from PyQt6.QtWidgets import QWidget
from utils import BACK_ARROW, CHANGE_PAGE, file_exists, default_image

class ShowCLient(QWidget, Ui_showClient):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_volver_show.setIcon(BACK_ARROW)
        self.bt_change_view_show.setIcon(CHANGE_PAGE)
    
    def setPic(self):
        ci = file_exists(self.cliente.ci, 'clients_pictures')
        if not ci:
            ci = DEFAULT_PICTURE
        default_image(self.lb_pic_client_show, ci, 'clients_pictures')

    def setClient(self, cliente: Clients):
        with Session() as session:
            self.cliente = session.merge(cliente)
            self.setPic()
            self.le_ci_show.setText(self.cliente.ci)
            self.le_phone_show.setText(self.cliente.phone)
            self.le_full_name_show.setText(self.cliente.nombre_apellidos)
            self.le_pais_show.setText(self.cliente.pais.pais)
            self.le_provincia_show.setText(self.cliente.municipio.provincia.provincia)
            self.le_municipio_show.setText(self.cliente.municipio.municipio)
            self.txted_notas_show.setText(self.cliente.notes)
            self.txted_alcance_show.setText(self.cliente.alcance)

    def setFunciones(self,funcVolver, funcChangePage):
        self.bt_volver_show.clicked.connect(funcVolver)
        self.bt_change_view_show.clicked.connect(funcChangePage)