# Form implementation generated from reading ui file 'd:\Programacion\Proyectos\Python\OnInk\onink\views\socials_usernamesui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_UsernamesSocials(object):
    def setupUi(self, UsernamesSocials):
        UsernamesSocials.setObjectName("UsernamesSocials")
        UsernamesSocials.resize(626, 418)
        self.verticalLayout = QtWidgets.QVBoxLayout(UsernamesSocials)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_13 = QtWidgets.QLabel(parent=UsernamesSocials)
        self.label_13.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(16)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("font-size: 16pt;")
        self.label_13.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.lb_cliente_name = QtWidgets.QLabel(parent=UsernamesSocials)
        self.lb_cliente_name.setMaximumSize(QtCore.QSize(16777215, 60))
        self.lb_cliente_name.setObjectName("lb_cliente_name")
        self.horizontalLayout_14.addWidget(self.lb_cliente_name)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem)
        self.bt_save_usernames = QtWidgets.QPushButton(parent=UsernamesSocials)
        self.bt_save_usernames.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\Programacion\\Proyectos\\Python\\OnInk\\onink\\views\\images/save.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_save_usernames.setIcon(icon)
        self.bt_save_usernames.setIconSize(QtCore.QSize(32, 32))
        self.bt_save_usernames.setObjectName("bt_save_usernames")
        self.horizontalLayout_14.addWidget(self.bt_save_usernames)
        self.verticalLayout.addLayout(self.horizontalLayout_14)
        self.verticalLySocials = QtWidgets.QVBoxLayout()
        self.verticalLySocials.setObjectName("verticalLySocials")
        self.verticalLayout.addLayout(self.verticalLySocials)
        spacerItem1 = QtWidgets.QSpacerItem(20, 312, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(UsernamesSocials)
        QtCore.QMetaObject.connectSlotsByName(UsernamesSocials)

    def retranslateUi(self, UsernamesSocials):
        _translate = QtCore.QCoreApplication.translate
        UsernamesSocials.setWindowTitle(_translate("UsernamesSocials", "Form"))
        self.label_13.setText(_translate("UsernamesSocials", "Redes sociales del cliente"))
        self.lb_cliente_name.setText(_translate("UsernamesSocials", "Cliente: "))
        self.bt_save_usernames.setText(_translate("UsernamesSocials", "Guardar"))
