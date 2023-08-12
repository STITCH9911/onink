import typing
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QDialog, QWidget, QMessageBox
from config import Session
from models import Productos, Io_productos
from views.io_productsDialog_ui import Ui_io_productsDialog

class IO_Products(QDialog, Ui_io_productsDialog):
    def __init__(self,mainwindow, producto: Productos, mode: str = 'out', parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.mode = mode
        self.producto = producto
        self.cantidad = 0
        self.timer_minus = QTimer()
        self.timer_plus = QTimer()
        self.timer_minus.setInterval(200)
        self.timer_plus.setInterval(200)
        self.timer_minus.timeout.connect(self.minus)
        self.le_cant.setText(str(self.cantidad))
        title = producto.nick
        self.mainwindow = mainwindow
        
        if mode == "in":
            operacion = "Entrada de productos"
            self.timer_plus.timeout.connect(self.plus_in)
            self.bt_plus.clicked.connect(self.plus_in)
        else:
            operacion = "Salida de productos"
            self.timer_plus.timeout.connect(self.plus_out)
            self.bt_plus.clicked.connect(self.plus_out)
        
        self.bt_minus.pressed.connect(self.timer_minus.start)
        self.bt_plus.pressed.connect(self.timer_plus.start)
        self.bt_minus.released.connect(self.timer_minus.stop)
        self.bt_plus.released.connect(self.timer_plus.stop)
        
        self.bt_minus.clicked.connect(self.minus)
        self.bt_cancel.clicked.connect(lambda: self.reject())
        self.bt_save.clicked.connect(self.save)
        self.lb_tittle.setText(title)
        self.lb_operacion.setText(operacion)
        self.lb_existencias.setText(str(producto.existencia))
        self.le_cant.setValidator(QIntValidator())
        self.le_cant.setReadOnly(True)
        self.setStyleSheet("""
        QFrame{
            background-color: rgb(54,72,100);
        }
        """)
        

    def save(self):
        cant = int(self.le_cant.text())
        if cant < 1:
            QMessageBox.critical(self.mainwindow, "Error", "El número de elementos de la operación deben ser 1 o mayor", QMessageBox.StandardButton.Ok)
            return
        
        with Session() as session:
            obj = session.merge(self.producto)
            if self.mode == "in":
                result = obj.existencia + cant
            else:
                result = obj.existencia - cant
            obj.existencia = result
            date = QDate.currentDate()
            io = Io_productos(io=self.mode, cant=cant, producto_id=obj.id, fecha=date.toPyDate())
            session.add(obj)
            session.add(io)
            session.commit()
        QMessageBox.information(self.mainwindow, "Correcto", "Operación completada de manera satisfactoria", QMessageBox.StandardButton.Ok)
        self.accept()

    def minus(self):
        if self.cantidad > 0:
            self.cantidad = self.cantidad - 1
            self.le_cant.setText(str(self.cantidad))

    def plus_in(self):
        self.cantidad = self.cantidad + 1
        self.le_cant.setText(str(self.cantidad))

    def plus_out(self):
        if self.cantidad < self.producto.existencia:
            self.plus_in()