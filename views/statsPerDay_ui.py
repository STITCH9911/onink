# Form implementation generated from reading ui file 'd:\Programacion\Proyectos\Python\OnInk\onink\views\statsPerDay.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_StatsDay(object):
    def setupUi(self, StatsDay):
        StatsDay.setObjectName("StatsDay")
        StatsDay.resize(400, 393)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(StatsDay)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(parent=StatsDay)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=StatsDay)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.cb_dia = QtWidgets.QComboBox(parent=StatsDay)
        self.cb_dia.setObjectName("cb_dia")
        self.horizontalLayout.addWidget(self.cb_dia)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 8)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=StatsDay)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.cb_mes = QtWidgets.QComboBox(parent=StatsDay)
        self.cb_mes.setObjectName("cb_mes")
        self.horizontalLayout_2.addWidget(self.cb_mes)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 8)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(parent=StatsDay)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.cb_anio = QtWidgets.QComboBox(parent=StatsDay)
        self.cb_anio.setObjectName("cb_anio")
        self.horizontalLayout_3.addWidget(self.cb_anio)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 8)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(parent=StatsDay)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.t_trabajos = QtWidgets.QLabel(parent=StatsDay)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.t_trabajos.setFont(font)
        self.t_trabajos.setText("")
        self.t_trabajos.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.t_trabajos.setObjectName("t_trabajos")
        self.verticalLayout.addWidget(self.t_trabajos)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_6 = QtWidgets.QLabel(parent=StatsDay)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.t_cash = QtWidgets.QLabel(parent=StatsDay)
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
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 2)
        self.verticalLayout_3.setStretch(2, 6)

        self.retranslateUi(StatsDay)
        QtCore.QMetaObject.connectSlotsByName(StatsDay)

    def retranslateUi(self, StatsDay):
        _translate = QtCore.QCoreApplication.translate
        StatsDay.setWindowTitle(_translate("StatsDay", "Form"))
        self.label.setText(_translate("StatsDay", "Estadísticas diarias"))
        self.label_2.setText(_translate("StatsDay", "Día:"))
        self.label_3.setText(_translate("StatsDay", "Mes:"))
        self.label_4.setText(_translate("StatsDay", "Año:"))
        self.label_5.setText(_translate("StatsDay", "Total de trabajos"))
        self.label_6.setText(_translate("StatsDay", "Total de dinero"))
