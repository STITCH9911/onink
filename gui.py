from PyQt6.QtGui import QDoubleValidator, QRegularExpressionValidator
from config import Session
from main_window_ui import Ui_OnInkMainWindow
from PyQt6.QtWidgets import QMainWindow, QSizeGrip, QMessageBox
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRegularExpression
from datetime import datetime
from models import Clients, Provincias, Municipios


class MainWindow(QMainWindow,Ui_OnInkMainWindow):
    def __init__(self, app, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        # Inicializar listas
        self.clientes, self.municipios, self.provincias = [], [], []
        # inicializar Item para editar
        self.item_selected = None

        self.gripSize = 10
        self.grip = QSizeGrip(self)
        self.grip.resize(self.gripSize,self.gripSize)
        self.bt_menu.clicked.connect(self.mover_menu)
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        self.bt_restaurar.hide()
        self.stackedWidget.setCurrentWidget(self.page_inicio)

        #Señales de CRUD Clientes
        self.bt_menu_clientes.clicked.connect(self.clients_list)
        self.bt_volver_cliente_c.clicked.connect(self.clients_list)
        self.bt_store_cliente.clicked.connect(self.clients_store)
        self.bt_create_cliente.clicked.connect(self.create_client)
        self.le_ci_insertar.setValidator(QDoubleValidator())
        self.le_telefono_insertar.setValidator(QDoubleValidator())
        self.le_nombre_apellidos_insertar.setValidator(QRegularExpressionValidator(QRegularExpression("[\D]+")))
        self.cb_provincia_insertar.currentIndexChanged.connect(self.change_provincia)
        self.bt_cliente_insertar_reestablecer.clicked.connect(self.reestablecer)
        
        self.setWindowOpacity(1)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)


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
    def clients_list(self):
        self.clear_le()
        with Session() as session:
            self.clientes = session.query(Clients).all()
            self.provincias = session.query(Provincias).all()
            self.municipios = session.query(Municipios).all()
            self.stackedWidget.setCurrentWidget(self.page_clientes)
    
    #metodo para ir a pagina de crear cliente
    def create_client(self):
        with Session() as session:
            self.provincias = session.query(Provincias).all()
            self.municipios = session.query(Municipios).all()
            self.stackedWidget.setCurrentWidget(self.page_insertar_cliente)
            self.load_combobox()

    #metodo en el que se crea un cliente
    def clients_store(self):
        with Session() as session:
            ci_list = session.query(Clients.ci).all()
            if self.le_ci_insertar.text() == "" or self.le_telefono_insertar.text() == "" or self.le_nombre_apellidos_insertar.text() == "" or self.cb_municipio_insertar.currentIndex() == -1:
                QMessageBox.critical(self,"Error", "Existen campos vacíos que debe llenar")
            elif self.le_ci_insertar in ci_list:
                QMessageBox.critical(self,"Error", "Existen un cliente con este número de identidad")
            elif not len(self.le_ci_insertar.text()) == 11:
                QMessageBox.critical(self,"Error", "El número de identidad debe de tener 11 dígitos")
            else:
                ci = self.le_ci_insertar.text()
                telefono = self.le_telefono_insertar.text()
                nombre_apellidos = self.le_nombre_apellidos_insertar.text()
                municipio = self.cb_municipio_insertar.currentData()
                created_at = datetime.now()
                notes = self.txtedt_notas_insertar.toPlainText()
                cliente = Clients(ci=ci, nombre_apellidos=nombre_apellidos, phone=telefono, municipio_id=municipio, notes=notes, created_at = created_at)
                session.add(cliente)
                session.commit()
                self.clients_list()
                QMessageBox.information(self, "Correcto", f"Agregado nuevo cliente: {cliente.nombre_apellidos} de forma exitosa.")
                
    #metodo para filtrar los municipios por provincia
    def change_provincia(self):
        provincia_id = self.cb_provincia_insertar.currentData()
        with Session() as session:
            if provincia_id:
                prov = session.query(Provincias).get(provincia_id)
                self.municipios = prov.municipios
            else:
                self.municipios = session.query(Municipios).all()
            self.load_combobox()

    #metodo para cargar todos los datos a los combobox
    def load_combobox(self):
        if self.page_insertar_cliente == self.stackedWidget.currentWidget():
            self.cb_municipio_insertar.clear()
            if self.cb_provincia_insertar.count() == 0:
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
    
    def reestablecer(self):
        if self.page_insertar_cliente == self.stackedWidget.currentWidget():
            self.cb_municipio_insertar.setCurrentIndex(-1)
            self.cb_provincia_insertar.setCurrentIndex(-1)
            self.load_combobox()
            self.clear_le()

    def clear_le(self):
        self.le_ci_insertar.clear()
        self.le_nombre_apellidos_insertar.clear()
        self.le_telefono_insertar.clear()
        self.txtedt_notas_insertar.clear()
        self.item_selected = None
        """ 
        self.le_ci_insertar.clear()
        self.le_ci_insertar.clear()
        self.le_ci_insertar.clear()
        self.le_ci_insertar.clear()
        self.le_ci_insertar.clear()
        self.le_ci_insertar.clear()
        self.le_ci_insertar.clear()
        self.le_ci_insertar.clear() """