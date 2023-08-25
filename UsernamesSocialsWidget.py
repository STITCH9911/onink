import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QWidget, QLineEdit, QMessageBox, QLabel, QHBoxLayout
from sqlalchemy import delete, insert, update
from config import Session
from models import Clients, Socials, t_r_clients_socials
from utils import ICON_SAVE
from views.socials_usernamesui_ui import Ui_UsernamesSocials

class UsernamesSocialWidget(QWidget,Ui_UsernamesSocials):
    def __init__(self, client: Clients, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.client = client
        self.mainWindowWidget  = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
        self.bt_save_usernames.clicked.connect(self.save_usernames)
        self.bt_save_usernames.setIcon(ICON_SAVE)

    def showEvent(self, a0) -> None:
        self.loadData()
        return super().showEvent(a0)
    
    def save_usernames(self):
        with Session() as session:
            self.socials = session.query(Socials).all()
            for social in self.socials:
                socialName = str(social.social).replace(" ", "_")
                line_edit = self.findChild(QLineEdit, f"le_{socialName}")
                q = session.query(t_r_clients_socials).filter_by(social_id=social.id, client_id=self.client.id).first()
                if line_edit.text() != "":
                    texto = line_edit.text()
                    if q and texto:
                        stmp = update(t_r_clients_socials).where(t_r_clients_socials.c.client_id == q.client_id, t_r_clients_socials.c.social_id == q.social_id).values(username=texto)
                        session.execute(stmp)
                    elif texto and not q:
                        stmp = insert(t_r_clients_socials).values(username=texto, client_id=self.client.id, social_id=social.id)
                        session.execute(stmp)
                elif q and not line_edit.text():
                    stmp = delete(t_r_clients_socials).where(t_r_clients_socials.c.client_id == q.client_id, t_r_clients_socials.c.social_id == q.social_id)
                    session.execute(stmp)
            session.commit()
        QMessageBox.information(self.mainWindowWidget, "Correcto", f"Ha actualizado los nombres de usuario para las redes sociales del cliente: {self.client.nombre_apellidos}")
        self.clients_list()

    def loadData(self):
        datas = dict()
        with Session() as session:
            socials = session.query(Socials).all()
            usernames = session.query(t_r_clients_socials).filter_by(client_id=self.client.id).all()
            for i in socials:
                datas[i.id] = ""
            for i in usernames:
                datas[i.social_id] = i.username
        
        for i in socials:
            label = QLabel(self)
            label.setText(f"{i.social} :")
            line_edit = QLineEdit(self)
            line_edit.setPlaceholderText(f"Nombre de usuario para {i.social}")
            line_edit.setText(str(datas[i.id]))
            socialName = str(i.social).replace(" ", "_")
            line_edit.setObjectName(f'le_{socialName}')
            hlayout = QHBoxLayout()
            hlayout.addWidget(label)
            hlayout.addWidget(line_edit)
            hlayout.setStretch(0,2)
            hlayout.setStretch(1,7)
            hlayout.setObjectName(f"layout_{socialName}")
            self.verticalLySocials.addLayout(hlayout)


    def clients_list(self):
        from ClientsList import ClientListWidget
        stacked = self.parentWidget()
        w = stacked.findChildren(ClientListWidget)
        for i in w:
            i.setParent(None)
        w = ClientListWidget(parent=stacked)
        stacked.addWidget(w)
        stacked.setCurrentWidget(w)