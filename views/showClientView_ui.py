# Form implementation generated from reading ui file 'd:\Programacion\Proyectos\Python\OnInk\onink\views\showClientView.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_showClient(object):
    def setupUi(self, showClient):
        showClient.setObjectName("showClient")
        showClient.resize(673, 629)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(showClient)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.bt_volver_show = QtWidgets.QPushButton(parent=showClient)
        self.bt_volver_show.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/back-arrow.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_volver_show.setIcon(icon)
        self.bt_volver_show.setIconSize(QtCore.QSize(32, 32))
        self.bt_volver_show.setObjectName("bt_volver_show")
        self.horizontalLayout_5.addWidget(self.bt_volver_show)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(parent=showClient)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.lb_pic_client_show = QtWidgets.QLabel(parent=showClient)
        self.lb_pic_client_show.setMinimumSize(QtCore.QSize(230, 230))
        self.lb_pic_client_show.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lb_pic_client_show.setStyleSheet("border: 3px solid white")
        self.lb_pic_client_show.setText("")
        self.lb_pic_client_show.setScaledContents(True)
        self.lb_pic_client_show.setObjectName("lb_pic_client_show")
        self.horizontalLayout_13.addWidget(self.lb_pic_client_show)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=showClient)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_ci_show = QtWidgets.QLineEdit(parent=showClient)
        self.le_ci_show.setReadOnly(True)
        self.le_ci_show.setObjectName("le_ci_show")
        self.horizontalLayout_2.addWidget(self.le_ci_show)
        self.horizontalLayout_2.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(parent=showClient)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.le_phone_show = QtWidgets.QLineEdit(parent=showClient)
        self.le_phone_show.setReadOnly(True)
        self.le_phone_show.setObjectName("le_phone_show")
        self.horizontalLayout_4.addWidget(self.le_phone_show)
        self.horizontalLayout_4.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(parent=showClient)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.le_pais_show = QtWidgets.QLineEdit(parent=showClient)
        self.le_pais_show.setReadOnly(True)
        self.le_pais_show.setObjectName("le_pais_show")
        self.horizontalLayout_6.addWidget(self.le_pais_show)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_6 = QtWidgets.QLabel(parent=showClient)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_11.addWidget(self.label_6)
        self.le_provincia_show = QtWidgets.QLineEdit(parent=showClient)
        self.le_provincia_show.setReadOnly(True)
        self.le_provincia_show.setObjectName("le_provincia_show")
        self.horizontalLayout_11.addWidget(self.le_provincia_show)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_8 = QtWidgets.QLabel(parent=showClient)
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_12.addWidget(self.label_8)
        self.le_municipio_show = QtWidgets.QLineEdit(parent=showClient)
        self.le_municipio_show.setReadOnly(True)
        self.le_municipio_show.setObjectName("le_municipio_show")
        self.horizontalLayout_12.addWidget(self.le_municipio_show)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_13.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=showClient)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.le_full_name_show = QtWidgets.QLineEdit(parent=showClient)
        self.le_full_name_show.setReadOnly(True)
        self.le_full_name_show.setObjectName("le_full_name_show")
        self.horizontalLayout.addWidget(self.le_full_name_show)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 8)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 14, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(parent=showClient)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.txted_notas_show = QtWidgets.QTextEdit(parent=showClient)
        self.txted_notas_show.setReadOnly(True)
        self.txted_notas_show.setObjectName("txted_notas_show")
        self.horizontalLayout_7.addWidget(self.txted_notas_show)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 8)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_9 = QtWidgets.QLabel(parent=showClient)
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.txted_alcance_show = QtWidgets.QTextEdit(parent=showClient)
        self.txted_alcance_show.setReadOnly(True)
        self.txted_alcance_show.setObjectName("txted_alcance_show")
        self.horizontalLayout_8.addWidget(self.txted_alcance_show)
        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 8)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem6)
        self.bt_change_view_show = QtWidgets.QPushButton(parent=showClient)
        self.bt_change_view_show.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/change (2).svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_change_view_show.setIcon(icon1)
        self.bt_change_view_show.setIconSize(QtCore.QSize(32, 32))
        self.bt_change_view_show.setObjectName("bt_change_view_show")
        self.horizontalLayout_9.addWidget(self.bt_change_view_show)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.retranslateUi(showClient)
        QtCore.QMetaObject.connectSlotsByName(showClient)

    def retranslateUi(self, showClient):
        _translate = QtCore.QCoreApplication.translate
        showClient.setWindowTitle(_translate("showClient", "Form"))
        self.bt_volver_show.setText(_translate("showClient", "Volver"))
        self.label_3.setText(_translate("showClient", "Datos del cliente"))
        self.label.setText(_translate("showClient", "CI: "))
        self.label_4.setText(_translate("showClient", "Teléfono: "))
        self.label_5.setText(_translate("showClient", "País:"))
        self.label_6.setText(_translate("showClient", "Provincia: "))
        self.label_8.setText(_translate("showClient", "Municipio: "))
        self.label_2.setText(_translate("showClient", "Nombre y apellidos: "))
        self.label_7.setText(_translate("showClient", "Notas: "))
        self.txted_notas_show.setPlaceholderText(_translate("showClient", "Sin notas"))
        self.label_9.setText(_translate("showClient", "Vía de llegada: "))
        self.txted_alcance_show.setPlaceholderText(_translate("showClient", "Sin información de como llegó hasta nosotros"))
        self.bt_change_view_show.setText(_translate("showClient", "Cambiar a datos de trabajos"))