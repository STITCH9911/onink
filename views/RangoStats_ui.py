# Form implementation generated from reading ui file 'd:\Programacion\Proyectos\Python\OnInk\onink\views\RangoStats.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_StatsPerRango(object):
    def setupUi(self, StatsPerRango):
        StatsPerRango.setObjectName("StatsPerRango")
        StatsPerRango.resize(687, 560)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(StatsPerRango)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(parent=StatsPerRango)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_7 = QtWidgets.QLabel(parent=StatsPerRango)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=StatsPerRango)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.cb_dia_inicio = QtWidgets.QComboBox(parent=StatsPerRango)
        self.cb_dia_inicio.setObjectName("cb_dia_inicio")
        self.horizontalLayout.addWidget(self.cb_dia_inicio)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 8)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=StatsPerRango)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.cb_mes_inicio = QtWidgets.QComboBox(parent=StatsPerRango)
        self.cb_mes_inicio.setObjectName("cb_mes_inicio")
        self.horizontalLayout_2.addWidget(self.cb_mes_inicio)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 8)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(parent=StatsPerRango)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.cb_anio_inicio = QtWidgets.QComboBox(parent=StatsPerRango)
        self.cb_anio_inicio.setObjectName("cb_anio_inicio")
        self.horizontalLayout_3.addWidget(self.cb_anio_inicio)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 8)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_10.addLayout(self.verticalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_8 = QtWidgets.QLabel(parent=StatsPerRango)
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_4.addWidget(self.label_8)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_9 = QtWidgets.QLabel(parent=StatsPerRango)
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_7.addWidget(self.label_9)
        self.cb_dia_fin = QtWidgets.QComboBox(parent=StatsPerRango)
        self.cb_dia_fin.setObjectName("cb_dia_fin")
        self.horizontalLayout_7.addWidget(self.cb_dia_fin)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 8)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_10 = QtWidgets.QLabel(parent=StatsPerRango)
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_8.addWidget(self.label_10)
        self.cb_mes_fin = QtWidgets.QComboBox(parent=StatsPerRango)
        self.cb_mes_fin.setObjectName("cb_mes_fin")
        self.horizontalLayout_8.addWidget(self.cb_mes_fin)
        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 8)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_11 = QtWidgets.QLabel(parent=StatsPerRango)
        self.label_11.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_9.addWidget(self.label_11)
        self.cb_anio_fin = QtWidgets.QComboBox(parent=StatsPerRango)
        self.cb_anio_fin.setObjectName("cb_anio_fin")
        self.horizontalLayout_9.addWidget(self.cb_anio_fin)
        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 8)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_9)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10.addLayout(self.verticalLayout_4)
        self.horizontalLayout_10.setStretch(0, 4)
        self.horizontalLayout_10.setStretch(1, 1)
        self.horizontalLayout_10.setStretch(2, 4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_12 = QtWidgets.QLabel(parent=StatsPerRango)
        self.label_12.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_11.addWidget(self.label_12)
        self.cb_trabajos = QtWidgets.QComboBox(parent=StatsPerRango)
        self.cb_trabajos.setObjectName("cb_trabajos")
        self.horizontalLayout_11.addWidget(self.cb_trabajos)
        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(1, 8)
        self.verticalLayout_5.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(parent=StatsPerRango)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.t_trabajos = QtWidgets.QLabel(parent=StatsPerRango)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.t_trabajos.setFont(font)
        self.t_trabajos.setText("")
        self.t_trabajos.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.t_trabajos.setObjectName("t_trabajos")
        self.verticalLayout.addWidget(self.t_trabajos)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_6 = QtWidgets.QLabel(parent=StatsPerRango)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.t_cash = QtWidgets.QLabel(parent=StatsPerRango)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.t_cash.setFont(font)
        self.t_cash.setText("")
        self.t_cash.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.t_cash.setObjectName("t_cash")
        self.verticalLayout_2.addWidget(self.t_cash)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5.setStretch(0, 4)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.bt_refresh = QtWidgets.QPushButton(parent=StatsPerRango)
        self.bt_refresh.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/refresh.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_refresh.setIcon(icon)
        self.bt_refresh.setIconSize(QtCore.QSize(35, 35))
        self.bt_refresh.setObjectName("bt_refresh")
        self.verticalLayout_5.addWidget(self.bt_refresh)

        self.retranslateUi(StatsPerRango)
        QtCore.QMetaObject.connectSlotsByName(StatsPerRango)

    def retranslateUi(self, StatsPerRango):
        _translate = QtCore.QCoreApplication.translate
        StatsPerRango.setWindowTitle(_translate("StatsPerRango", "Form"))
        self.label.setText(_translate("StatsPerRango", "Estadísticas por rango"))
        self.label_7.setText(_translate("StatsPerRango", "Fecha inicio"))
        self.label_2.setText(_translate("StatsPerRango", "Día:"))
        self.label_3.setText(_translate("StatsPerRango", "Mes:"))
        self.label_4.setText(_translate("StatsPerRango", "Año:"))
        self.label_8.setText(_translate("StatsPerRango", "Fecha fin"))
        self.label_9.setText(_translate("StatsPerRango", "Día:"))
        self.label_10.setText(_translate("StatsPerRango", "Mes:"))
        self.label_11.setText(_translate("StatsPerRango", "Año:"))
        self.label_12.setText(_translate("StatsPerRango", "Trabajos: "))
        self.cb_trabajos.setPlaceholderText(_translate("StatsPerRango", "Todos"))
        self.label_5.setText(_translate("StatsPerRango", "Total de trabajos"))
        self.label_6.setText(_translate("StatsPerRango", "Total de dinero"))
        self.bt_refresh.setText(_translate("StatsPerRango", "Refrescar"))
