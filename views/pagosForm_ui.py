# Form implementation generated from reading ui file 'd:\Programacion\Proyectos\Python\OnInk\onink\views\pagosForm.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_pagosForm(object):
    def setupUi(self, pagosForm):
        pagosForm.setObjectName("pagosForm")
        pagosForm.resize(494, 424)
        pagosForm.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(pagosForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bt_back = QtWidgets.QPushButton(parent=pagosForm)
        self.bt_back.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/back-arrow.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_back.setIcon(icon)
        self.bt_back.setIconSize(QtCore.QSize(32, 32))
        self.bt_back.setObjectName("bt_back")
        self.horizontalLayout.addWidget(self.bt_back)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.bt_title = QtWidgets.QPushButton(parent=pagosForm)
        self.bt_title.setMinimumSize(QtCore.QSize(0, 0))
        self.bt_title.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.bt_title.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.bt_title.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/credit-card white.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_title.setIcon(icon1)
        self.bt_title.setIconSize(QtCore.QSize(100, 100))
        self.bt_title.setObjectName("bt_title")
        self.verticalLayout.addWidget(self.bt_title)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=pagosForm)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(parent=pagosForm)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 8)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.bt_save = QtWidgets.QPushButton(parent=pagosForm)
        self.bt_save.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/save.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_save.setIcon(icon2)
        self.bt_save.setIconSize(QtCore.QSize(32, 32))
        self.bt_save.setObjectName("bt_save")
        self.horizontalLayout_3.addWidget(self.bt_save)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(pagosForm)
        QtCore.QMetaObject.connectSlotsByName(pagosForm)

    def retranslateUi(self, pagosForm):
        _translate = QtCore.QCoreApplication.translate
        pagosForm.setWindowTitle(_translate("pagosForm", "Form"))
        self.bt_back.setText(_translate("pagosForm", "Volver"))
        self.label_2.setText(_translate("pagosForm", "Tipo de pago: "))
        self.lineEdit.setPlaceholderText(_translate("pagosForm", "Tipo de pago"))
        self.bt_save.setText(_translate("pagosForm", "Guardar"))
