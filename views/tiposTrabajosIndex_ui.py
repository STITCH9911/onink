# Form implementation generated from reading ui file 'd:\Programacion\Proyectos\Python\OnInk\onink\views\tiposTrabajosIndex.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_tiposTrabajosIndex(object):
    def setupUi(self, tiposTrabajosIndex):
        tiposTrabajosIndex.setObjectName("tiposTrabajosIndex")
        tiposTrabajosIndex.resize(604, 459)
        self.verticalLayout = QtWidgets.QVBoxLayout(tiposTrabajosIndex)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=tiposTrabajosIndex)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.layoutFiltro = QtWidgets.QHBoxLayout()
        self.layoutFiltro.setObjectName("layoutFiltro")
        self.label_2 = QtWidgets.QLabel(parent=tiposTrabajosIndex)
        self.label_2.setObjectName("label_2")
        self.layoutFiltro.addWidget(self.label_2)
        self.le_search = QtWidgets.QLineEdit(parent=tiposTrabajosIndex)
        self.le_search.setObjectName("le_search")
        self.layoutFiltro.addWidget(self.le_search)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.layoutFiltro.addItem(spacerItem)
        self.bt_create = QtWidgets.QPushButton(parent=tiposTrabajosIndex)
        self.bt_create.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/icons8-plus-24.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_create.setIcon(icon)
        self.bt_create.setIconSize(QtCore.QSize(32, 32))
        self.bt_create.setObjectName("bt_create")
        self.layoutFiltro.addWidget(self.bt_create)
        self.verticalLayout.addLayout(self.layoutFiltro)
        self.layout_tabla = QtWidgets.QHBoxLayout()
        self.layout_tabla.setObjectName("layout_tabla")
        self.verticalLayout.addLayout(self.layout_tabla)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 7)

        self.retranslateUi(tiposTrabajosIndex)
        QtCore.QMetaObject.connectSlotsByName(tiposTrabajosIndex)

    def retranslateUi(self, tiposTrabajosIndex):
        _translate = QtCore.QCoreApplication.translate
        tiposTrabajosIndex.setWindowTitle(_translate("tiposTrabajosIndex", "Form"))
        self.label.setText(_translate("tiposTrabajosIndex", "Tipos de trabajos"))
        self.label_2.setText(_translate("tiposTrabajosIndex", "Buscar: "))
        self.le_search.setPlaceholderText(_translate("tiposTrabajosIndex", "Buscar..."))
        self.bt_create.setText(_translate("tiposTrabajosIndex", "Agregar nuevo"))