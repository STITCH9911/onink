# Form implementation generated from reading ui file 'd:\Programacion\Proyectos\Python\OnInk\onink\views\ClientsListWidget.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ClientsListWidget(object):
    def setupUi(self, ClientsListWidget):
        ClientsListWidget.setObjectName("ClientsListWidget")
        ClientsListWidget.resize(561, 441)
        self.verticalLayout = QtWidgets.QVBoxLayout(ClientsListWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(parent=ClientsListWidget)
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(16)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("font-size: 16pt;")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.bt_create_cliente = QtWidgets.QPushButton(parent=ClientsListWidget)
        self.bt_create_cliente.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/add-client.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_create_cliente.setIcon(icon)
        self.bt_create_cliente.setIconSize(QtCore.QSize(25, 25))
        self.bt_create_cliente.setObjectName("bt_create_cliente")
        self.horizontalLayout_3.addWidget(self.bt_create_cliente)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 5)
        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(3, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_14 = QtWidgets.QLabel(parent=ClientsListWidget)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_15.addWidget(self.label_14)
        self.le_search_clients = QtWidgets.QLineEdit(parent=ClientsListWidget)
        self.le_search_clients.setObjectName("le_search_clients")
        self.horizontalLayout_15.addWidget(self.le_search_clients)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem2)
        self.bt_refresh_search_clients = QtWidgets.QPushButton(parent=ClientsListWidget)
        self.bt_refresh_search_clients.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/refresh.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_refresh_search_clients.setIcon(icon1)
        self.bt_refresh_search_clients.setIconSize(QtCore.QSize(32, 32))
        self.bt_refresh_search_clients.setObjectName("bt_refresh_search_clients")
        self.horizontalLayout_15.addWidget(self.bt_refresh_search_clients)
        self.verticalLayout.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setSpacing(11)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_15 = QtWidgets.QLabel(parent=ClientsListWidget)
        self.label_15.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_16.addWidget(self.label_15)
        self.cb_search_clientes_pais = QtWidgets.QComboBox(parent=ClientsListWidget)
        self.cb_search_clientes_pais.setObjectName("cb_search_clientes_pais")
        self.horizontalLayout_16.addWidget(self.cb_search_clientes_pais)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem3)
        self.horizontalLayout_19.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_16 = QtWidgets.QLabel(parent=ClientsListWidget)
        self.label_16.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_17.addWidget(self.label_16)
        self.cb_search_clientes_provincia = QtWidgets.QComboBox(parent=ClientsListWidget)
        self.cb_search_clientes_provincia.setObjectName("cb_search_clientes_provincia")
        self.horizontalLayout_17.addWidget(self.cb_search_clientes_provincia)
        self.horizontalLayout_19.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem4)
        self.label_18 = QtWidgets.QLabel(parent=ClientsListWidget)
        self.label_18.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_18.addWidget(self.label_18)
        self.cb_search_clientes_municipio = QtWidgets.QComboBox(parent=ClientsListWidget)
        self.cb_search_clientes_municipio.setObjectName("cb_search_clientes_municipio")
        self.horizontalLayout_18.addWidget(self.cb_search_clientes_municipio)
        self.horizontalLayout_19.addLayout(self.horizontalLayout_18)
        self.verticalLayout.addLayout(self.horizontalLayout_19)
        self.tableLayout = QtWidgets.QVBoxLayout()
        self.tableLayout.setObjectName("tableLayout")
        self.verticalLayout.addLayout(self.tableLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 6)

        self.retranslateUi(ClientsListWidget)
        QtCore.QMetaObject.connectSlotsByName(ClientsListWidget)

    def retranslateUi(self, ClientsListWidget):
        _translate = QtCore.QCoreApplication.translate
        ClientsListWidget.setWindowTitle(_translate("ClientsListWidget", "Form"))
        self.label_3.setText(_translate("ClientsListWidget", "Gestión de clientes"))
        self.bt_create_cliente.setText(_translate("ClientsListWidget", "Agregar nuevo"))
        self.label_14.setText(_translate("ClientsListWidget", "Buscar: "))
        self.le_search_clients.setPlaceholderText(_translate("ClientsListWidget", "Buscar..."))
        self.bt_refresh_search_clients.setToolTip(_translate("ClientsListWidget", "<html><head/><body><p>Reiniciar filtros de búsqueda</p></body></html>"))
        self.label_15.setText(_translate("ClientsListWidget", "Pais: "))
        self.cb_search_clientes_pais.setPlaceholderText(_translate("ClientsListWidget", "País..."))
        self.label_16.setText(_translate("ClientsListWidget", "Provincia: "))
        self.cb_search_clientes_provincia.setPlaceholderText(_translate("ClientsListWidget", "Provincia..."))
        self.label_18.setText(_translate("ClientsListWidget", "Municipio: "))
        self.cb_search_clientes_municipio.setPlaceholderText(_translate("ClientsListWidget", "Municipio"))
