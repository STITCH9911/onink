import os, shutil
from typing import List
from PyQt6.QtGui import QDoubleValidator, QRegularExpressionValidator, QPixmap, QIcon, QShowEvent
from config import DEFAULT_PICTURE, Session, PICTURES_DIR
from materialesControllers import MaterialForm, MaterialIndex
from municipiosController import MunicipiosForm, MunicipiosIndex
from socialsIndex import SocialsIndex, SocialsWidgetCreate
from strippedTable import StripedTable
from ClientWorks import ClientWorks
from showClient import ShowCLient
from homeController import Home
from tecnicasControllers import TecnicaForm, TecnicaIndex
from viewsPaises import PaisesWidget, PaisesWidgetCreate
from provinciasControllers import ProvinciasIndex, ProvinciasForm
from tonoControllers import TonosIndex, TonoForm
from pagosControllers import PagoIndex, PagosForm
from trabajosController import TrabajosIndex, TrabajoForm
from tiposTrabajosControllers import TiposTrabajosIndex, TiposTrabajosForm
from views.main_window_ui import Ui_OnInkMainWindow
from PyQt6.QtWidgets import QMainWindow, QSizeGrip, QMessageBox, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRegularExpression, QSize, pyqtSlot
from datetime import datetime
from models import Clients, Provincias, Municipios, Paises, Socials, Turnos, t_r_clients_socials, t_r_trabajos_materiales, Trabajos
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from utils import file_exists, delete_file, default_image

class MainWindow(QMainWindow,Ui_OnInkMainWindow):
    def __init__(self, app, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.icono = QIcon()
        self.setWindowIcon(self.icono)

        #widgets
        self.strippedTable = None
        self.home = Home(self.stackedWidget)
        self.qWidgetShowClient = ShowCLient()
        self.CWorks = ClientWorks()
        self.WPaises = PaisesWidget(self.stackedWidget)
        self.CreatePaisesWidget = PaisesWidgetCreate(self.stackedWidget)
        self.SocialWidgetForm = SocialsWidgetCreate(self.stackedWidget)
        self.IndexSocial = SocialsIndex(self.stackedWidget)
        self.ProvinciasIndex = ProvinciasIndex(self.stackedWidget)
        self.ProvinciasForm = ProvinciasForm(self.stackedWidget)
        self.MunicipiosIndex = MunicipiosIndex(self.stackedWidget)
        self.MunicipiosForm = MunicipiosForm(self.stackedWidget)
        self.TonoIndex = TonosIndex(self.stackedWidget)
        self.TonoForm = TonoForm(self.stackedWidget)
        self.pago_page = PagoIndex(self.stackedWidget)
        self.pago_form = PagosForm(self.stackedWidget)
        self.tecnica_page = TecnicaIndex(self.stackedWidget)
        self.tecnica_form = TecnicaForm(self.stackedWidget)
        self.material_page = MaterialIndex(self.stackedWidget)
        self.material_form = MaterialForm(self.stackedWidget)
        self.TrabajosIndex = TrabajosIndex(self.stackedWidget)
        self.TrabajosForm = TrabajoForm(self.stackedWidget)
        self.TiposTrabajosIndex = TiposTrabajosIndex(self.stackedWidget)
        self.TiposTrabajosForm = TiposTrabajosForm(self.stackedWidget)

        #add widgets a stackedWidget
        self.stackedWidget.addWidget(self.home)
        self.stackedWidget.addWidget(self.WPaises)
        self.stackedWidget.addWidget(self.qWidgetShowClient)
        self.stackedWidget.addWidget(self.CWorks)
        self.stackedWidget.addWidget(self.CreatePaisesWidget)
        self.stackedWidget.addWidget(self.SocialWidgetForm)
        self.stackedWidget.addWidget(self.IndexSocial)
        self.stackedWidget.addWidget(self.ProvinciasForm)
        self.stackedWidget.addWidget(self.ProvinciasIndex)
        self.stackedWidget.addWidget(self.MunicipiosIndex)
        self.stackedWidget.addWidget(self.MunicipiosForm)
        self.stackedWidget.addWidget(self.TonoIndex)
        self.stackedWidget.addWidget(self.TonoForm)
        self.stackedWidget.addWidget(self.pago_page)
        self.stackedWidget.addWidget(self.pago_form)
        self.stackedWidget.addWidget(self.tecnica_page)
        self.stackedWidget.addWidget(self.tecnica_form)
        self.stackedWidget.addWidget(self.material_page)
        self.stackedWidget.addWidget(self.material_form)
        self.stackedWidget.addWidget(self.TrabajosIndex)
        self.stackedWidget.addWidget(self.TrabajosForm)
        self.stackedWidget.addWidget(self.TiposTrabajosIndex)
        self.stackedWidget.addWidget(self.TiposTrabajosForm)
        
        #establecer widgetInicial
        self.stackedWidget.setCurrentWidget(self.home)

        # Inicializar listas
        with Session() as session:
            self.clientes, self.municipios, self.provincias, self.paises, self.socials = [], [], [], session.query(Paises).all(), [],
        
        # inicializar Item para editar
        self.item_selected = None

        #datos de las imagenes
        self.file_name = None
        self.send_image = False

        #Boton de resize window
        self.gripSize = 10
        self.grip = QSizeGrip(self)
        self.grip.resize(self.gripSize,self.gripSize)

        #acciones del frame superior
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        self.bt_restaurar.hide()

        #btMenus
        self.bt_menu_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.home))
        self.bt_menu.clicked.connect(self.mover_menu)
        self.bt_menu_clientes.clicked.connect(self.clients_list)
        self.bt_menu_paises.clicked.connect(self.paisesIndex)
        self.bt_menu_sociales.clicked.connect(self.socialIndex)
        self.bt_menu_provincias.clicked.connect(self.provincias_index)
        self.bt_menu_municipios.clicked.connect(self.municipios_index)
        self.bt_menu_tonos.clicked.connect(self.tonos_index)
        self.bt_menu_pagos.clicked.connect(self.pagos_index)
        self.bt_menu_tecnicas.clicked.connect(self.tecnicas_index)
        self.bt_menu_materiales.clicked.connect(self.materiales_index)
        self.bt_menu_trabajos.clicked.connect(self.trabajos_index)


        #Señales de CRUD Clientes
        self.createClient = True
        self.bt_volver_cliente_c.clicked.connect(self.clients_list)
        self.bt_store_cliente.clicked.connect(self.clients_store)
        self.bt_create_cliente.clicked.connect(self.create_client)
        self.le_ci_insertar.setValidator(QDoubleValidator())
        self.le_telefono_insertar.setValidator(QDoubleValidator())
        self.le_nombre_apellidos_insertar.setValidator(QRegularExpressionValidator(QRegularExpression("[\D]+")))
        self.cb_provincia_insertar.currentIndexChanged.connect(lambda: self.change_provincia(self.cb_provincia_insertar))
        self.cb_search_clientes_provincia.currentIndexChanged.connect(lambda: self.change_provincia(self.cb_search_clientes_provincia))
        self.bt_cliente_insertar_reestablecer.clicked.connect(self.reestablecer)
        self.bt_add_image_clients_insert.clicked.connect(lambda: self.select_image(label=self.lb_pic_insert_cliente))
        self.bt_delete_image_clients_insert.clicked.connect(self.restart_image)
        self.bt_save_usernames.clicked.connect(self.save_usernames)
        self.le_search_clients.textChanged.connect(self.search)
        self.cb_search_clientes_municipio.currentIndexChanged.connect(lambda: self.change_municipio(self.cb_search_clientes_municipio))
        self.cb_search_clientes_pais.currentIndexChanged.connect(lambda: self.change_pais(self.cb_search_clientes_pais))
        self.bt_refresh_search_clients.clicked.connect(self.refresh)
        
        #config de la ventana
        self.setWindowOpacity(1)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)

    #reiniciar imagen
    def restart_image(self):
        default_image(self.lb_pic_insert_cliente, DEFAULT_PICTURE, "clients_pictures")
        self.send_image = False

    #Evento abrir ventana
    def showEvent(self, a0: QShowEvent) -> None:
        print("INICIANDO APLICACIÓN")
        return super().showEvent(a0)

    #Evento de cerrar ventana
    def closeEvent(self, event):
        print("PROGRAMA FINALIZADO")
        event.accept()
    
    #evento de reajuste de tamanno
    def resizeEvent(self, event) -> None:
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    #evento de presionar boton de mouse
    def mousePressEvent(self, event) -> None:
        self.click_position = event.globalPosition().toPoint()

    #metodo para mover la ventana
    def mover_ventana(self,event):
        if self.isMaximized() == False:
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.click_position)
                self.click_position = event.globalPosition().toPoint()
                event.accept()
            if event.globalPosition().y() <= 10:
                self.showMaximized()
                self.bt_maximizar.hide()
                self.bt_restaurar.show()
            else:
                self.showNormal()
                self.bt_maximizar.show()
                self.bt_restaurar.hide()

    #metodo para animacion de menu
    def mover_menu(self):
        width = self.frame_control.width()
        normal = 0

        if width == 0:
            extender = 200
        else:
            extender = normal
        
        self.animacion = QPropertyAnimation(self.frame_control, b'minimumWidth')
        self.animacion.setDuration(400)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animacion.start()

    #metodo para ir a pagina de listado de clientes
    @pyqtSlot()
    def clients_list(self):
        self.clear_le()
        with Session() as session:
            self.clientes = session.query(Clients).all()
            self.provincias = session.query(Provincias).all()
            self.municipios = session.query(Municipios).all()
            self.paises = session.query(Paises).all()
            headers, data, dropdowns_buttons, clients = self.getClientsDataTable(self.clientes)
            self.stackedWidget.setCurrentWidget(self.page_clientes)
            # Borrar la tabla existente y crear una nueva tabla con los nuevos datos
            if self.strippedTable is not None:
                self.verticalLayout_page_clientes.removeWidget(self.strippedTable)
                self.strippedTable.clearContents()
            self.strippedTable = StripedTable(headers, data, dropdowns_buttons, clients)
            self.verticalLayout_page_clientes.addWidget(self.strippedTable)
            self.cb_search_clientes_municipio.setCurrentIndex(-1)
            self.cb_search_clientes_pais.setCurrentIndex(-1)
            self.cb_search_clientes_provincia.setCurrentIndex(-1)
            self.le_search_clients.setText("")
            self.load_combobox()
    
    #metodo para resfrescar
    def refresh(self):
        if self.stackedWidget.currentWidget() == self.page_clientes:
            self.cb_search_clientes_provincia.setCurrentIndex(-1)
            self.cb_search_clientes_municipio.setCurrentIndex(-1)
            self.cb_search_clientes_municipio.setCurrentIndex(-1)
            self.le_search_clients.setText("")
            self.load_combobox()
            self.search()

    #metodo para ir a pagina de crear cliente
    def create_client(self):
        self.createClient = True
        self.le_ci_insertar.setReadOnly(False)
        self.bt_cliente_insertar_reestablecer.show()
        with Session() as session:
            self.provincias = session.query(Provincias).all()
            self.municipios = session.query(Municipios).all()
            self.paises = session.query(Paises).all()
            self.stackedWidget.setCurrentWidget(self.page_insertar_cliente)
            default_image(self.lb_pic_insert_cliente, DEFAULT_PICTURE, "clients_pictures")
            self.send_image = False
            self.cb_pais_insertar.clear()
            self.load_combobox()

    #metodo en el que se crea un cliente
    def clients_store(self):
        with Session() as session:
            ci_list = session.query(Clients.ci).all()
            if self.le_ci_insertar.text() == "" or self.le_telefono_insertar.text() == "" or self.le_nombre_apellidos_insertar.text() == "" or (self.cb_municipio_insertar.currentIndex() == -1 and self.cb_pais_insertar.currentIndex == -1):
                QMessageBox.critical(self,"Error", "Existen campos vacíos que debe llenar")                
            elif not len(self.le_ci_insertar.text()) == 11:
                QMessageBox.critical(self,"Error", "El número de identidad debe de tener 11 dígitos")
            else:
                ci = self.le_ci_insertar.text()
                telefono = self.le_telefono_insertar.text()
                nombre_apellidos = self.le_nombre_apellidos_insertar.text()
                municipio = self.cb_municipio_insertar.currentData()
                created_at = datetime.now()
                notes = self.txtedt_notas_insertar.toPlainText()
                pais_id = self.cb_pais_insertar.currentData()
                alcance = self.txedt_alcance.toPlainText()
                if self.createClient:
                    cliente = Clients(ci=ci, nombre_apellidos=nombre_apellidos, phone=telefono, municipio_id=municipio, notes=notes, created_at = created_at, pais_id=pais_id, alcance=alcance)
                else:
                    cliente = self.item_selected
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
                    QMessageBox.critical(self,"Error", "Existen un cliente con este número de identidad")
                    session.rollback()
                    return
                
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Redes Sociales")
                msg_box.setText("¿Desea administrar las redes sociales para el nuevo cliente?. Esta acción puede realizarse en otro momento.")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
                msg_box.button(QMessageBox.StandardButton.Yes).setText("Sí")
                msg_box.button(QMessageBox.StandardButton.No).setText("No")
                reply = msg_box.exec()
                if reply == QMessageBox.StandardButton.Yes:
                    self.item_selected = cliente
                    self.add_usernames_socials()
                else:
                    self.clients_list()
                    if self.createClient:
                        texto = f"Agregado nuevo cliente: {cliente.nombre_apellidos} de forma exitosa."
                    else:
                        texto = f"Editado datos personales del cliente: {cliente.nombre_apellidos} de forma exitosa."
                    QMessageBox.information(self, "Correcto", texto)
                
    #metodo para filtrar los municipios por provincia
    def change_provincia(self, combobox: QComboBox):
        provincia_id = combobox.currentData()
        with Session() as session:
            if provincia_id:
                prov = session.query(Provincias).get(provincia_id)
                self.municipios = prov.municipios
            else:
                self.municipios = session.query(Municipios).all()
            self.load_combobox()
        self.search()

    #metodo para filtrar por municipio
    def change_municipio(self, combobox: QComboBox):
        municipio_id = combobox.currentData()
        if municipio_id:
            self.search()

    #metodo para filtrar por pais:
    def change_pais(self, combobox:QComboBox):
        pais_id = combobox.currentData()
        if pais_id:
            self.search()

    #metodo para cargar todos los datos a los combobox
    def load_combobox(self):

        if self.page_insertar_cliente == self.stackedWidget.currentWidget():
            self.cb_municipio_insertar.clear()
            if len(self.paises) != self.cb_pais_insertar.count():
                self.cb_pais_insertar.clear()
                for pais in self.paises:
                    self.cb_pais_insertar.addItem(pais.pais, pais.id)
            if self.cb_provincia_insertar.count() != len(self.provincias):
                self.cb_provincia_insertar.clear()
                for prov in self.provincias:
                    self.cb_provincia_insertar.addItem(prov.provincia, prov.id)
            if len(self.municipios) == 0:
                self.cb_municipio_insertar.setCurrentIndex(-1)
                self.cb_municipio_insertar.setPlaceholderText("Sin resultados")
            else:
                self.cb_municipio_insertar.setPlaceholderText("Seleccionar municipio")
                self.cb_municipio_insertar.setCurrentIndex(-1)
                for mun in self.municipios:
                    self.cb_municipio_insertar.addItem(mun.municipio, mun.id)

        if self.page_clientes == self.stackedWidget.currentWidget():
            self.cb_search_clientes_municipio.clear()
            self.cb_search_clientes_pais.clear()
            for pais in self.paises:
                self.cb_search_clientes_pais.addItem(pais.pais, pais.id)
            if self.cb_search_clientes_provincia.count() != len(self.provincias):
                self.cb_search_clientes_provincia.clear()
                for prov in self.provincias:
                    self.cb_search_clientes_provincia.addItem(prov.provincia, prov.id)
            self.cb_search_clientes_municipio.setCurrentIndex(-1)
            if len(self.municipios) == 0:
                self.cb_search_clientes_municipio.setPlaceholderText("Sin resultados")
            else:
                self.cb_search_clientes_municipio.setPlaceholderText("Municipio")
                for mun in self.municipios:
                    self.cb_search_clientes_municipio.addItem(mun.municipio, mun.id)
                
    #metodo para reestablecer los campos a su valor por defecto
    def reestablecer(self):
        if self.page_insertar_cliente == self.stackedWidget.currentWidget():
            self.cb_municipio_insertar.setCurrentIndex(-1)
            self.cb_provincia_insertar.setCurrentIndex(-1)
            self.cb_pais_insertar.setCurrentIndex(-1)
            default_image(label=self.lb_pic_insert_cliente, default=DEFAULT_PICTURE, dir="clients_pictures")
            self.send_image = False
            self.load_combobox()
            self.clear_le()

    #metodo para estables los QLineEdit y QTextEdit a vacios
    def clear_le(self):
        self.le_ci_insertar.clear()
        self.le_nombre_apellidos_insertar.clear()
        self.le_telefono_insertar.clear()
        self.txtedt_notas_insertar.clear()
        self.txedt_alcance.clear()
        self.item_selected = None

    #Funcion para seleccionar la imagen y mostrar la previsualizacion
    def select_image(self, label):
        file_name,_ = QFileDialog.getOpenFileName(self, "Seleccione la imagen",PICTURES_DIR,"Archivos de imagen (*.png *.jpg *.jpeg)")
        if file_name:
            pixmap = QPixmap(file_name)
            label.setPixmap(pixmap.scaled(label.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
            self.file_name = file_name
            self.send_image = True

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

    #metodo para aeliminar ocntenido de un layout
    def eliminar_contenido(self, contenedor):
        while contenedor.count():
            item = contenedor.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                sublayout = item.layout()
                if sublayout is not None:
                    self.eliminar_contenido(sublayout)
                contenedor.removeItem(item)
    
    #metodo para agregar los campos para nombres de usuarios de redes sociales de un cliente
    def add_usernames_socials(self, **karg):
        with Session() as session:
            client_name = f"Cliente: {self.item_selected.nombre_apellidos}"
            self.lb_cliente_name.setText(client_name)
            self.socials = session.query(Socials).all()
            self.eliminar_contenido(self.verticalLySocials)
            for social in self.socials:

                label = QLabel(self.page_add_social_usernames)
                label.setText(social.social+": ")
                line_edit = QLineEdit(self.page_add_social_usernames)
                line_edit.setPlaceholderText(f"Nombre de usuario para {social.social}")
                line_edit.setObjectName(f'le_{social.social}')
                if social.social in karg:
                    line_edit.setText(karg[social.social])
                hlayout = QHBoxLayout()
                hlayout.addWidget(label)
                hlayout.addWidget(line_edit)
                hlayout.setStretch(0,2)
                hlayout.setStretch(1,7)
                hlayout.setObjectName(f"layout_{social.social.replace(' ','_')}")
                self.verticalLySocials.addLayout(hlayout)

        self.stackedWidget.setCurrentWidget(self.page_add_social_usernames)

    #metodo para crear,actualizar y eliminar los nombres de usuario de un cliente
    def save_usernames(self):
        with Session() as session:
            self.socials = session.query(Socials).all()
            for social in self.socials:
                line_edit = self.page_add_social_usernames.findChild(QLineEdit, f"le_{social.social}")
                q = session.query(t_r_clients_socials).filter_by(social_id=social.id, client_id=self.item_selected.id).first()
                if line_edit.text() != "":
                    texto = line_edit.text()
                    if q and texto:
                        stmp = update(t_r_clients_socials).where(t_r_clients_socials.c.client_id == q.client_id, t_r_clients_socials.c.social_id == q.social_id).values(username=texto)
                        session.execute(stmp)
                    elif texto and not q:
                        stmp = insert(t_r_clients_socials).values(username=texto, client_id=self.item_selected.id, social_id=social.id)
                        session.execute(stmp)
                elif q and not line_edit.text():
                    stmp = delete(t_r_clients_socials).where(t_r_clients_socials.c.client_id == q.client_id, t_r_clients_socials.c.social_id == q.social_id)
                    session.execute(stmp)
            session.commit()
        QMessageBox.information(self, "Correcto", f"Ha actualizado los nombres de usuario para las redes sociales del cliente: {self.item_selected.nombre_apellidos}")
        self.item_selected = None
        self.clients_list()

    #metodo para abrir la vista de los nombres de usuarios de redes sociales
    def edit_usernames_socials(self, client: Clients):
        with Session() as session:
            client = session.merge(client)
            self.item_selected = client
            usernames = {}
            socials = client.social
            for social in socials:
                username = session.query(t_r_clients_socials.c.username).filter_by(client_id = client.id, social_id=social.id).first()
                if username:
                    usernames[social.social] = username[0]
        self.add_usernames_socials(**usernames)

    #metodo para editar datos personales del cliente
    def edit_client_data(self, client: Clients):
        self.createClient = False
        self.bt_cliente_insertar_reestablecer.hide()
        with Session() as session:
            client = session.merge(client)
            self.item_selected = client
            self.le_ci_insertar.setText(client.ci)
            self.le_ci_insertar.setReadOnly(True)
            self.le_nombre_apellidos_insertar.setText(client.nombre_apellidos)
            self.le_telefono_insertar.setText(client.phone)
            self.stackedWidget.setCurrentWidget(self.page_insertar_cliente)
            self.load_combobox()
            if client.pais_id:
                index = self.cb_pais_insertar.findData(client.pais_id)
                self.cb_pais_insertar.setCurrentIndex(index)
            indexP = self.cb_provincia_insertar.findData(client.municipio.provincia_id)
            self.cb_provincia_insertar.setCurrentIndex(indexP)
            indexM = self.cb_municipio_insertar.findData(client.municipio_id)
            self.cb_municipio_insertar.setCurrentIndex(indexM)
            self.txedt_alcance.setPlainText(client.alcance)
            self.txtedt_notas_insertar.setPlainText(client.notes)
            file_name = file_exists(client.ci, 'clients_pictures')
            if not file_name:
                file_name = DEFAULT_PICTURE
            default_image(self.lb_pic_insert_cliente, file_name, 'clients_pictures')
            self.send_image = False
            
    #metodo para eliminar un cliente
    def delete_client(self, client: Clients):
        with Session() as session:
            client = session.query(Clients).get(client.id)
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Eliminar registro")
            msg_box.setText(f"Está a punto de eliminar al cliente \"{client.nombre_apellidos}\". Este registro no podrá ser recuperado.\n¿Desea continuar?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            msg_box.button(QMessageBox.StandardButton.Yes).setText("Sí")
            msg_box.button(QMessageBox.StandardButton.No).setText("No")
            reply = msg_box.exec()
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
        self.clients_list()

    #obtener elementos para tabla de clientes
    def getClientsDataTable(self, clients: List['Clients']):
        with Session() as session:

            headers = ["CI", "Nombre y Apellidos", "País","Municipio", "Opciones"]
            data = []
            dropdown_buttons = []
            for client in clients:
                client = session.merge(client)
                pais = "-"
                if client.pais:
                    pais = client.pais.pais
                data.append([client.ci, client.nombre_apellidos, pais, client.municipio.municipio])
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
                    {"Eliminar": self.delete_client, trash : size}
                ]
                dropdown_buttons.append(buttons)

            return headers, data, dropdown_buttons, clients
    
    #metodo para recargar tabla
    def reload_table(self, collection: list):
        if self.page_clientes == self.stackedWidget.currentWidget():
            headers, data, dropdowns_buttons, objects = self.getClientsDataTable(collection)
            st = self.strippedTable
            self.strippedTable.close()
            layout = self.verticalLayout_page_clientes
            layout.removeWidget(st)
            self.strippedTable = StripedTable(headers, data, dropdowns_buttons, objects)
            layout.addWidget(self.strippedTable)

    #metodo para realizar la busqueda de elementos en la tabla
    def search(self):
        if self.stackedWidget.currentWidget() == self.page_clientes:
            with Session() as session:

                text = self.le_search_clients.text()
                pais_id = self.cb_search_clientes_pais.currentData()
                provincia_id = self.cb_search_clientes_provincia.currentData()
                municipio_id = self.cb_search_clientes_municipio.currentData()
                clients = session.query(Clients).join(Municipios, Municipios.id == Clients.municipio_id).join(Provincias, Provincias.id == Municipios.provincia_id).join(Paises, Paises.id == Clients.pais_id)
                if text != "" and not text.isdigit():
                    clients = clients.filter(Clients.nombre_apellidos.like(f"%{text}%"))
                elif text.isdigit():
                    clients = clients.filter(Clients.ci.like(f"%{text}%"))
                if pais_id:
                    clients = clients.filter(Clients.pais_id == pais_id)
                if provincia_id:
                    clients = clients.filter(Municipios.provincia_id == provincia_id)
                if municipio_id:
                    clients = clients.filter(Clients.municipio_id == municipio_id)
                
                clients = clients.all()                    
            self.reload_table(clients)
    
    #metodo para visualizar datos del cliente
    def showClienteData(self, client: Clients):
        self.qWidgetShowClient.setFunciones(self.clients_list, lambda: self.client_works(client))
        self.qWidgetShowClient.setClient(client)
        self.stackedWidget.setCurrentWidget(self.qWidgetShowClient)

    #metodo para ver los trabajos de un cliente
    def client_works(self, client: Clients):
        self.CWorks.setFunciones(self.clients_list, lambda: self.showClienteData(client))
        self.CWorks.setClient(client)
        self.stackedWidget.setCurrentWidget(self.CWorks)

    #metodo para ver la lista de paises
    def paisesIndex(self):
        self.WPaises.set_functions(self.editPais)
        self.WPaises.search()
        self.stackedWidget.setCurrentWidget(self.WPaises)

    #metodo para ver editar pais
    def editPais(self,obj):
        self.CreatePaisesWidget.setPais(obj)
        self.stackedWidget.setCurrentWidget(self.CreatePaisesWidget)

    #metodo para ver lista de redes sociales
    def socialIndex(self):
        self.IndexSocial.search()
        self.stackedWidget.setCurrentWidget(self.IndexSocial)

    #metodo para ver listad de provincias
    def provincias_index(self):
        self.ProvinciasIndex.search()
        self.stackedWidget.setCurrentWidget(self.ProvinciasIndex)

    #metodo para ver lista de municipios
    def municipios_index(self):
        self.MunicipiosIndex.load_cb()
        self.MunicipiosIndex.search()
        self.stackedWidget.setCurrentWidget(self.MunicipiosIndex)

    #metodo para ver la lista de tonos
    def tonos_index(self):
        self.TonoIndex.search()
        self.stackedWidget.setCurrentWidget(self.TonoIndex)

    #metodo para ver la lista de pagos
    def pagos_index(self):
        self.pago_page.search()
        self.stackedWidget.setCurrentWidget(self.pago_page)

    #metodo para ver listado de tecnicas
    def tecnicas_index(self):
        self.tecnica_page.search()
        self.stackedWidget.setCurrentWidget(self.tecnica_page)

    #metodo para ver listado de materiales
    def materiales_index(self):
        self.material_page.search()
        self.stackedWidget.setCurrentWidget(self.material_page)

    #metodo para ver listado de trabajos
    def trabajos_index(self):
        self.stackedWidget.setCurrentWidget(self.TrabajosIndex)