# Form implementation generated from reading ui file 'd:\Programacion\Proyectos\Python\OnInk\onink\views\productsIndex.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ProductosIndex(object):
    def setupUi(self, ProductosIndex):
        ProductosIndex.setObjectName("ProductosIndex")
        ProductosIndex.resize(740, 477)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProductosIndex)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=ProductosIndex)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=ProductosIndex)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.le_search = QtWidgets.QLineEdit(parent=ProductosIndex)
        self.le_search.setObjectName("le_search")
        self.horizontalLayout.addWidget(self.le_search)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.bt_add = QtWidgets.QPushButton(parent=ProductosIndex)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/icons8-plus-24.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_add.setIcon(icon)
        self.bt_add.setIconSize(QtCore.QSize(35, 35))
        self.bt_add.setObjectName("bt_add")
        self.horizontalLayout_2.addWidget(self.bt_add)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tablaLayout = QtWidgets.QVBoxLayout()
        self.tablaLayout.setObjectName("tablaLayout")
        self.verticalLayout.addLayout(self.tablaLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 6)

        self.retranslateUi(ProductosIndex)
        QtCore.QMetaObject.connectSlotsByName(ProductosIndex)

    def retranslateUi(self, ProductosIndex):
        _translate = QtCore.QCoreApplication.translate
        ProductosIndex.setWindowTitle(_translate("ProductosIndex", "Form"))
        self.label.setText(_translate("ProductosIndex", "Productos"))
        self.label_2.setText(_translate("ProductosIndex", "Buscar:"))
        self.le_search.setPlaceholderText(_translate("ProductosIndex", "Buscar..."))
        self.bt_add.setText(_translate("ProductosIndex", "Nuevo producto"))
