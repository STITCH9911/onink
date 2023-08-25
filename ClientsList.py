import os
from typing import List
from PyQt6.QtCore import QSize
from sqlalchemy import delete
from utils import ADD_CLIENT, REFRESH, eliminar_contenido
from views.ClientsListWidget_ui import Ui_ClientsListWidget
from PyQt6.QtWidgets import QWidget, QMessageBox, QStackedWidget
from PyQt6.QtGui import QShowEvent
from config import Session
from models import Clients, Municipios, Paises, Provincias, t_r_clients_socials,Trabajos, Turnos,t_r_trabajos_materiales
from strippedTable import StripedTable

class ClientListWidget(QWidget, Ui_ClientsListWidget):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.bt_create_cliente.setIcon(ADD_CLIENT)
        self.bt_refresh_search_clients.setIcon(REFRESH)
        self.bt_create_cliente.clicked.connect(self.create_client)
        self.cb_search_clientes_municipio.currentIndexChanged.connect(self.search_municipios)
        self.cb_search_clientes_pais.currentIndexChanged.connect(self.search_paises)
        self.cb_search_clientes_provincia.currentIndexChanged.connect(self.search_provincias)
        self.le_search_clients.textChanged.connect(self.search)
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
        self.bt_refresh_search_clients.clicked.connect(self.refresh)

    #Evento de mostrar widget
    def showEvent(self, a0: QShowEvent) -> None:
        self.load_cb()
        self.create_table()
        return super().showEvent(a0)
    
    
    #generar tabla
    def create_table(self):
        headers, data, dropdowns_buttons, clients = self.getClientsDataTable(self.Clientes())
        tabla = StripedTable(headers,data,dropdowns_buttons,clients)
        eliminar_contenido(self.tableLayout)
        self.tableLayout.addWidget(tabla)
  
    #cargar datos en QComboBox municipios, provincias, paises con todos (all)
    def load_cb(self):
        with Session() as session:
            paises = session.query(Paises).all()
            prov = session.query(Provincias).all()
            municipios = session.query(Municipios).all()
        
        self.loadPaises(paises)
        self.loadProvincias(prov)
        self.loadMunicipios(municipios)

    #obtener clientes (filtrados o no)
    def Clientes(self)->List['Clients']:
        pais = self.cb_search_clientes_pais.currentData()
        provincia = self.cb_search_clientes_provincia.currentData()
        municipio = self.cb_search_clientes_municipio.currentData()
        search = self.le_search_clients.text()
        with Session() as session:
            q = session.query(Clients)
            if provincia:
                q = q.select_from(Clients).join(Municipios).filter(Municipios.provincia_id == provincia)
            if search != "":
                if search.isdigit():
                    q = q.filter(Clients.ci.like(f"%{search}%"))
                else:
                    q = q.filter(Clients.nombre_apellidos.like(f"%{search}%"))
            if pais:
                q = q.filter(Clients.pais_id == pais)
           
            if municipio:
                q = q.filter(Clients.municipio_id == municipio)
            
            q = q.all()
        return q
    
    #cargar datos en QComboBox porvincias
    def loadPaises(self, paises):
        self.cb_search_clientes_pais.clear()
        self.cb_search_clientes_pais.setCurrentIndex(-1)
        for i in paises:
            self.cb_search_clientes_pais.addItem(i.pais, i.id)

    #cargar datos en QComboBox provinicas
    def loadProvincias(self, provincias):
        self.cb_search_clientes_provincia.clear()
        self.cb_search_clientes_provincia.setCurrentIndex(-1)
        for i in provincias:
            self.cb_search_clientes_provincia.addItem(i.provincia,i.id)
    
    #cargar datos en QComboBox municipios
    def loadMunicipios(self,municipios):
        self.cb_search_clientes_municipio.clear()
        self.cb_search_clientes_municipio.setCurrentIndex(-1)
        for i in municipios:
            self.cb_search_clientes_municipio.addItem(i.municipio, i.id)

    #obtener elementos para tabla de clientes
    def getClientsDataTable(self, clients: List['Clients']):
        with Session() as session:
            headers = ["CI", "Nombre y Apellidos", "País","Municipio", "Opciones"]
            data = []
            dropdown_buttons = []

            for client in clients:
                client = session.merge(client)
                pais = "-"
                municipio = '-'
                if client.pais:
                    pais = client.pais.pais
                if client.municipio:
                    municipio = client.municipio.municipio
                data.append([client.ci, client.nombre_apellidos, pais, municipio])
                size = QSize(30,30)
                dir = 'views/images'
                edit = os.path.join(dir, 'edit-pencil.svg')
                trash = os.path.join(dir, 'trash.svg')
                social = os.path.join(dir, 'social-network.svg')
                show = os.path.join(dir, 'eye.svg')
                service = os.path.join(dir, 'services-portfolio.svg')
                buttons = [
                    {"Ver detalles": self.showClienteData, show: size},
                    {"Editar datos": self.edit_client_data, edit : size},
                    {"Redes sociales": self.edit_usernames_socials, social: size},
                    {"Servicios": self.client_works, service: size},
                    {"Nuevo trabajo": self.newWorkClient, service:size},
                    {"Eliminar": self.delete_client, trash : size}
                ]
                dropdown_buttons.append(buttons)

            return headers, data, dropdown_buttons, clients
        
    #metodo para eliminar un cliente
    def delete_client(self, client: Clients):
        with Session() as session:
            client = session.query(Clients).get(client.id)
            reply = QMessageBox.warning(self.mainWindowWidget, "Eliminar registro", f"Está a punto de eliminar al cliente \"{client.nombre_apellidos}\". Este registro no podrá ser recuperado.\n¿Desea continuar?", QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                stmp = delete(t_r_clients_socials).where(t_r_clients_socials.c.client_id == client.id)
                session.execute(stmp)
                q = session.query(Trabajos).join(Clients).filter(Clients.id == client.id).all()
                for toDelete in q:
                    stmp = delete(t_r_trabajos_materiales).where(t_r_trabajos_materiales.c.trabajo_id == toDelete.id)
                    session.execute(stmp)
                q = session.query(Turnos).filter_by(cliente_id= client.id).all()
                for toDelete in q:
                    session.delete(toDelete)
                session.delete(client)
                session.commit()
        self.create_table()

    def showClienteData(self, client: Clients):
        from showClient import ShowCLient
        stacked: QStackedWidget = self.parentWidget()
        w = stacked.findChildren(ShowCLient)
        for i in w:
            i.setParent(None)
        p = stacked.findChildren(ShowCLient)
        w = ShowCLient(parent=stacked, client=client)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)

    def edit_client_data(self, client: Clients):
        from ClientStore import ClientStoreWidget
        stacked: QStackedWidget = self.parentWidget()
        w = stacked.findChildren(ClientStoreWidget)
        for i in w:
            i.setParent(None)
        w = ClientStoreWidget(parent=stacked, client=client)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)

    def edit_usernames_socials(self, client: Clients):
        from UsernamesSocialsWidget import UsernamesSocialWidget
        stacked: QStackedWidget = self.parentWidget()
        w = stacked.findChildren(UsernamesSocialWidget)
        for i in w:
            i.setParent(None)
        w = UsernamesSocialWidget(parent=stacked, client=client)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)
    
    def client_works(self, client:Clients):
        from ClientWorks import ClientWorks
        stacked: QStackedWidget = self.parentWidget()
        w = stacked.findChildren(ClientWorks)
        for i in w:
            i.setParent(None)
        w = ClientWorks(parent=stacked, client=client)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)

    def newWorkClient(self, client: Clients):
        stacked = self.parentWidget()
        from trabajosController import TrabajoForm
        w = stacked.findChild(TrabajoForm)
        w.refresh()
        w.load_cb()
        w.setClient(client)
        stacked.setCurrentWidget(w)

    def create_client(self):
        from ClientStore import ClientStoreWidget
        stacked: QStackedWidget = self.parentWidget()
        w = stacked.findChildren(ClientStoreWidget)
        for i in w:
            i.setParent(None)
        w = ClientStoreWidget(parent=stacked)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)

    def search_provincias(self):
        provincia = self.cb_search_clientes_provincia.currentData()
        with Session() as session:
            q = session.query(Municipios).filter(Municipios.provincia_id == provincia).all()

        self.loadMunicipios(q)
        self.create_table()
    
    def search_paises(self):
        self.create_table()
    
    def search_municipios(self):
        self.create_table()
    
    def search(self):
        self.create_table()
    
    def refresh(self):
        self.load_cb()
        self.le_search_clients.clear()
        self.create_table()