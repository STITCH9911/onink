from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap

import os


def get_birthday(ci: str) -> QDate:
    fecha_str = ci[:6]

    fecha = QDate.fromString(fecha_str, "yyMMdd")  # crear objeto QDate a partir de la cadena de fecha

    hoy = QDate.currentDate()  # obtener la fecha actual

    if fecha.year() > hoy.year() % 100:
        fecha = fecha.addYears(-100)  # si la fecha es del futuro, restar 100 años

    return fecha

def get_age(ci):
    fecha_nacimiento = get_birthday(ci=ci)
    hoy = QDate.currentDate()
    return fecha_nacimiento.daysTo(hoy) // 365

def file_exists(name: str, folder: str = 'clients_pictures') -> str|bool:
    for file_name in os.listdir(folder):
        file_base, file_ext = os.path.splitext(file_name)
        if file_base == name:
            return file_name
    return False

def delete_file(name: str, folder: str = 'clients_pictures'):
    if file_exists(name,folder):
        file_path = os.path.join(folder,file_exists(name,folder))
        os.remove(file_path)

#metodo para establecer la imagen por defecto
def default_image(label: QLabel, default: str, dir: str):
    file_name = os.path.join(dir,default)
    pixmap = QPixmap(file_name)
    label.setPixmap(pixmap.scaled(label.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))