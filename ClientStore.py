from typing import List
from PyQt6.QtGui import QDoubleValidator, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression
from config import DEFAULT_PICTURE, PICTURES_DIR, Session
from models import Clients, Paises, Municipios, Provincias
from utils import BACK_ARROW, ICON_SAVE, REFRESH, UPLOAD_PICTURE, default_image, file_exists, delete_file
from views.ClientStoreui_ui import Ui_ClientStore
from PyQt6.QtWidgets import QWidget, QMessageBox, QLabel, QFileDialog
from PyQt6.QtGui import QPixmap
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import os, shutil

class ClientStoreWidget(QWidget, Ui_ClientStore):
    def __init__(self, client: Clients | None = None, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        #signals
        self.bt_volver_cliente_c.clicked.connect(self.back)
        self.bt_add_image_clients_insert.clicked.connect(self.select_image)
        self.bt_delete_image_clients_insert.clicked.connect(self.restart_image)
        self.bt_cliente_insertar_reestablecer.clicked.connect(self.reestablecer)
        self.le_ci_insertar.setValidator(QDoubleValidator())
        self.le_telefono_insertar.setValidator(QDoubleValidator())
        self.le_nombre_apellidos_insertar.setValidator(QRegularExpressionValidator(QRegularExpression("[\D]+")))
        self.bt_store_cliente.clicked.connect(self.clients_store)
        self.cb_provincia_insertar.currentIndexChanged.connect(self.change_prov)

        #inicializar data
        self.client = client
        self.send_image = False
        self.file_name = None
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()

        #icons
        self.bt_volver_cliente_c.setIcon(BACK_ARROW)
        self.bt_add_image_clients_insert.setIcon(UPLOAD_PICTURE)
        self.bt_store_cliente.setIcon(ICON_SAVE)
        self.bt_delete_image_clients_insert.setIcon(REFRESH)
        self.bt_cliente_insertar_reestablecer.setIcon(REFRESH)
        

    def change_prov(self):
        prov = self.cb_provincia_insertar.currentData()
        with Session() as session:
            if prov != None:
                p = session.query(Provincias).get(prov)
                municipios = p.municipios
            else:
                municipios = session.query(Municipios).all()
        self.loadMunicipios(municipios)

    def showEvent(self, a0) -> None:
        self.reestablecer()
        return super().showEvent(a0)
    #reiniciar imagen
    def restart_image(self):
        default_image(self.lb_pic_insert_cliente, DEFAULT_PICTURE, "clients_pictures")
        self.send_image = False

    def clients_store(self):
        with Session() as session:
            if self.validar():
                ci = self.le_ci_insertar.text()
                telefono = self.le_telefono_insertar.text()
                nombre_apellidos = self.le_nombre_apellidos_insertar.text()
                municipio = self.cb_municipio_insertar.currentData()
                created_at = datetime.now()
                notes = self.txtedt_notas_insertar.toPlainText()
                pais_id = self.cb_pais_insertar.currentData()
                alcance = self.txedt_alcance.toPlainText()
                if self.client == None:
                    cliente = Clients(ci=ci, nombre_apellidos=nombre_apellidos, phone=telefono, municipio_id=municipio, notes=notes, created_at = created_at, pais_id=pais_id, alcance=alcance)
                else:
                    cliente = self.client
                    cliente.ci = ci
                    cliente.nombre_apellidos = nombre_apellidos
                    cliente.phone = telefono
                    cliente.municipio_id = municipio
                    cliente.notes = notes
                    cliente.pais_id = pais_id
                    cliente.alcance = alcance
                self.save_image(dir="clients_pictures", label=self.lb_pic_insert_cliente, name=ci)
                session.add(cliente)
                try:
                    session.commit()
                except IntegrityError:
                    QMessageBox.critical(self.mainWindowWidget,"Error", "Existen un cliente con este número de identidad")
                    session.rollback()
                    return
                reply = None
                if self.client == None:
                    reply = QMessageBox.information(self.mainWindowWidget, "Redes Sociales", "¿Desea administrar las redes sociales para el nuevo cliente?. Esta acción puede realizarse en otro momento.", QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    self.socialsUpdate(cliente)
                else:
                    if self.client == None:
                        texto = f"Agregado nuevo cliente: {cliente.nombre_apellidos} de forma exitosa."
                    else:
                        texto = f"Editado datos personales del cliente: {cliente.nombre_apellidos} de forma exitosa."
                    QMessageBox.information(self.mainWindowWidget, "Correcto", texto)
                    self.back()

    def validar(self):
            if self.le_ci_insertar.text() == "" or self.le_telefono_insertar.text() == "" or self.le_nombre_apellidos_insertar.text() == "" or (self.cb_municipio_insertar.currentIndex() == -1 and self.cb_pais_insertar.currentIndex == -1):
                QMessageBox.critical(self.mainWindowWidget,"Error", "Existen campos vacíos que debe llenar")
                return False
            elif not len(self.le_ci_insertar.text()) == 11:
                QMessageBox.critical(self.mainWindowWidget,"Error", "El número de identidad debe de tener 11 dígitos")
                return False
            return True

    #reiniciar imagen
    def restart_image(self):
        default_image(self.lb_pic_insert_cliente, DEFAULT_PICTURE, "clients_pictures")
        self.send_image = False 

    #metodo para guardar una imagen
    def save_image(self, dir: str, label: QLabel, name:str):
        if self.send_image:
            file_name = self.file_name
            if file_name:
                if not os.path.exists(dir):
                    os.mkdir(dir)
            new_file_name = os.path.join(dir, name + os.path.splitext(os.path.basename(file_name))[1])
            if file_exists(name,dir):
                delete_file(name, dir)
            shutil.copy(file_name, new_file_name)
            default_image(label,DEFAULT_PICTURE, 'clients_pictures')
            self.send_image = False
    
    #metodo para reestablecer los campos a su valor por defecto
    def reestablecer(self):
        self.send_image = False
        self.load_combobox()
        self.clear_le()

    def load_combobox(self):
        with Session() as session:
            paises = session.query(Paises).all()
            provincias = session.query(Provincias).all()
            municipios = session.query(Municipios).all()

        self.loadPaises(paises)
        self.loadProvincias(provincias)
        self.loadMunicipios(municipios)

    def loadPaises(self,paises: List['Paises']):
        self.cb_pais_insertar.clear()
        if len(paises) > 0:
            ph = "Seleccione"
        else:
            ph = "Sin resultados"
        self.cb_pais_insertar.setPlaceholderText(ph)
        for i in paises:
            self.cb_pais_insertar.addItem(i.pais, i.id)
        self.cb_pais_insertar.setCurrentIndex(-1)
        
    def loadProvincias(self,provincias: List['Provincias']):
        self.cb_provincia_insertar.clear()
        if len(provincias) > 0:
            ph = "Seleccione"
        else:
            ph = "Sin resultados"
        self.cb_provincia_insertar.setPlaceholderText(ph)
        for i in provincias:
            self.cb_provincia_insertar.addItem(i.provincia, i.id)
        self.cb_provincia_insertar.setCurrentIndex(-1)
        
    def loadMunicipios(self,municipios: List['Municipios']):
        self.cb_municipio_insertar.clear()
        if len(municipios) > 0:
            ph = "Seleccione"
        else:
            ph = "Sin resultados"
        self.cb_municipio_insertar.setPlaceholderText(ph)
        for i in municipios:
            self.cb_municipio_insertar.addItem(i.municipio, i.id)
        self.cb_municipio_insertar.setCurrentIndex(-1)
        
    def clear_le(self):
        self.send_image = False
        if self.client:
            self.le_ci_insertar.setText(str(self.client.ci))
            self.le_nombre_apellidos_insertar.setText(self.client.nombre_apellidos)
            self.le_telefono_insertar.setText(str(self.client.phone))
            self.txedt_alcance.setText(str(self.client.alcance))
            self.txtedt_notas_insertar.setText(str(self.client.notes))
            self.cb_municipio_insertar.setCurrentIndex(self.cb_municipio_insertar.findData(self.client.municipio_id))
            self.cb_pais_insertar.setCurrentIndex(self.cb_pais_insertar.findData(self.client.pais_id))
            filename = file_exists(self.client.ci)
            if filename:
                default_image(label=self.lb_pic_insert_cliente, default=file_exists(self.client.ci), dir="clients_pictures")
            else:
                default_image(label=self.lb_pic_insert_cliente, default=DEFAULT_PICTURE, dir="clients_pictures")
                
        else:
            default_image(label=self.lb_pic_insert_cliente, default=DEFAULT_PICTURE, dir="clients_pictures")
            self.le_ci_insertar.clear()
            self.le_nombre_apellidos_insertar.clear()
            self.le_telefono_insertar.clear()
            self.txtedt_notas_insertar.clear()
            self.txedt_alcance.clear()

    #Funcion para seleccionar la imagen y mostrar la previsualizacion
    def select_image(self):
        file_name,_ = QFileDialog.getOpenFileName(self, "Seleccione la imagen",PICTURES_DIR,"Archivos de imagen (*.png *.jpg *.jpeg)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.lb_pic_insert_cliente.setPixmap(pixmap.scaled(self.lb_pic_insert_cliente.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
            self.file_name = file_name
            self.send_image = True

    def socialsUpdate(self, client):
        from UsernamesSocialsWidget import UsernamesSocialWidget
        stacked = self.parentWidget()
        w = stacked.findChildren(UsernamesSocialWidget)
        for i in w:
            i.setParent(None)
        w = UsernamesSocialWidget(parent=stacked, client=client)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)

    def back(self):
        from ClientsList import ClientListWidget
        stacked = self.parentWidget()
        w = stacked.findChild(ClientListWidget)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)