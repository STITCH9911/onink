from materialesControllers import MaterialForm, MaterialIndex
from municipiosController import MunicipiosForm, MunicipiosIndex
from productosWidget import ProductosForm, ProductosIndex
from rangoStatsWidgets import RangoStats
from socialsIndex import SocialsIndex, SocialsWidgetCreate
from stadisticsPerDay import StatsDay
from statsProducts import StatsProd
from homeController import Home
from tecnicasControllers import TecnicaForm, TecnicaIndex
from viewsPaises import PaisesWidget, PaisesWidgetCreate
from provinciasControllers import ProvinciasIndex, ProvinciasForm
from tonoControllers import TonosIndex, TonoForm
from pagosControllers import PagoIndex, PagosForm
from trabajosController import TrabajosIndex, TrabajoForm
from tiposTrabajosControllers import TiposTrabajosIndex, TiposTrabajosForm
from views.main_window_ui import Ui_OnInkMainWindow
from PyQt6.QtWidgets import QMainWindow, QSizeGrip
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from utils import CLOSE, COUNTRY, HOME, MATERIALS, MAXIMIZE, MINIMIZE, MUNICIPIOS, PAGOS, PRODUCTOS, PROVINCIAS, RESTAURAR, SERVICE, SIDEBAR_MENU, SOCIAL, STATS, TECNICAS, TONOS, USER

class MainWindow(QMainWindow,Ui_OnInkMainWindow):
    def __init__(self, app, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        #Buttons_icons
        self.bt_close.setIcon(CLOSE)
        self.bt_maximizar.setIcon(MAXIMIZE)
        self.bt_minimizar.setIcon(MINIMIZE)
        self.bt_restaurar.setIcon(RESTAURAR)
        self.bt_menu.setIcon(SIDEBAR_MENU)
        self.bt_menu_home.setIcon(HOME)
        self.bt_menu_clientes.setIcon(USER)
        self.bt_menu_trabajos.setIcon(SERVICE)
        self.bt_menu_sociales.setIcon(SOCIAL)
        self.bt_menu_paises.setIcon(COUNTRY)
        self.bt_menu_provincias.setIcon(PROVINCIAS)
        self.bt_menu_municipios.setIcon(MUNICIPIOS)
        self.bt_menu_materiales.setIcon(MATERIALS)
        self.bt_menu_tecnicas.setIcon(TECNICAS)
        self.bt_menu_tonos.setIcon(TONOS)
        self.bt_menu_pagos.setIcon(PAGOS)
        self.bt_stats.setIcon(STATS)
        self.bt_productos.setIcon(PRODUCTOS)
        
        
        #widgets
        self.home = Home(self.stackedWidget)
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
        self.statsDay = StatsDay(self.stackedWidget)
        self.productosIndex = ProductosIndex(self.stackedWidget)
        self.productosForm = ProductosForm(self.stackedWidget)
        self.rangoWidget = RangoStats(self.stackedWidget)
        self.statsProducts = StatsProd(self.stackedWidget)

        #add widgets a stackedWidget
        self.stackedWidget.addWidget(self.home)
        self.stackedWidget.addWidget(self.WPaises)
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
        self.stackedWidget.addWidget(self.statsDay)
        self.stackedWidget.addWidget(self.productosIndex)
        self.stackedWidget.addWidget(self.productosForm)
        self.stackedWidget.addWidget(self.rangoWidget)
        self.stackedWidget.addWidget(self.statsProducts)
        
        #establecer widgetInicial
        self.stackedWidget.setCurrentWidget(self.home)

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
        self.bt_menu_clientes.clicked.connect(self.clienList)
        self.bt_menu_paises.clicked.connect(self.paisesIndex)
        self.bt_menu_sociales.clicked.connect(self.socialIndex)
        self.bt_menu_provincias.clicked.connect(self.provincias_index)
        self.bt_menu_municipios.clicked.connect(self.municipios_index)
        self.bt_menu_tonos.clicked.connect(self.tonos_index)
        self.bt_menu_pagos.clicked.connect(self.pagos_index)
        self.bt_menu_tecnicas.clicked.connect(self.tecnicas_index)
        self.bt_menu_materiales.clicked.connect(self.materiales_index)
        self.bt_menu_trabajos.clicked.connect(self.trabajos_index)
        self.bt_stats.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_stats))
        self.bt_productos.clicked.connect(self.productIndex)
        self.bt_stats_day.clicked.connect(self.statsDayIndex)
        self.bt_stats_rango.clicked.connect(self.rangoIndex)
        self.bt_stats_productos.clicked.connect(self.statsproductosIndex)
        
        #config de la ventana
        self.setWindowOpacity(1)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)

    #
    def clienList(self):
        from ClientsList import ClientListWidget
        w = self.stackedWidget.findChildren(ClientListWidget)
        for i in w:
            i.setParent(None)
        w = ClientListWidget(parent=self.stackedWidget)
        self.stackedWidget.addWidget(w)
        self.stackedWidget.setCurrentWidget(w)

    #Evento abrir ventana
    def showEvent(self, a0) -> None:
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

    def productIndex(self):
        self.productosIndex.search()
        self.stackedWidget.setCurrentWidget(self.productosIndex)

    def statsDayIndex(self):
        self.statsDay.loadData()
        self.stackedWidget.setCurrentWidget(self.statsDay)

    def rangoIndex(self):
        self.rangoWidget.loadData()
        self.stackedWidget.setCurrentWidget(self.rangoWidget)

    def statsproductosIndex(self):
        self.statsProducts.loadData()
        self.stackedWidget.setCurrentWidget(self.statsProducts)