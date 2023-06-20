from PyQt6.QtGui import QIntValidator
from main_window_ui import Ui_OnInkMainWindow
from PyQt6.QtWidgets import QMainWindow, QSizeGrip
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve


class MainWindow(QMainWindow,Ui_OnInkMainWindow):
    def __init__(self, app, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.gripSize = 10
        self.grip = QSizeGrip(self)
        self.grip.resize(self.gripSize,self.gripSize)

        self.le_ci_insertar.setValidator(QIntValidator())
        self.le_telefono_insertar.setValidator(QIntValidator())

        self.bt_restaurar.hide()
        self.stackedWidget.setCurrentWidget(self.page_inicio)
        self.bt_menu_clientes.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_clientes))
        self.bt_create_cliente.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_insertar_cliente))
        self.bt_volver_cliente_c.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_clientes))
        self.bt_menu.clicked.connect(self.mover_menu)
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        self.setWindowOpacity(1)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)

    def resizeEvent(self, event) -> None:
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event) -> None:
        self.click_position = event.globalPosition().toPoint()

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
