from PyQt6.QtCore import QDate, Qt, QTimer
from PyQt6.QtWidgets import QLabel, QProgressDialog
from PyQt6.QtGui import QPixmap, QIcon
import functools
from time import sleep

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


#Iconos
IMAGES_ROUTE = 'views/images'
ICON_SAVE = QIcon(os.path.join(IMAGES_ROUTE, 'save.svg'))
CLOSE = QIcon(os.path.join(IMAGES_ROUTE, 'close.svg'))
RESTAURAR = QIcon(os.path.join(IMAGES_ROUTE, 'restaurar.svg'))
MINIMIZE = QIcon(os.path.join(IMAGES_ROUTE, 'minimize.svg'))
MAXIMIZE = QIcon(os.path.join(IMAGES_ROUTE, 'maximize.svg'))
SIDEBAR_MENU = QIcon(os.path.join(IMAGES_ROUTE, 'sidebar-menu.svg'))
CANCEL = QIcon(os.path.join(IMAGES_ROUTE, 'cancel.svg'))
HOME = QIcon(os.path.join(IMAGES_ROUTE, 'home (1).svg'))
SERVICE = QIcon(os.path.join(IMAGES_ROUTE, 'services-portfolio.svg'))
SOCIAL = QIcon(os.path.join(IMAGES_ROUTE, 'social-network.svg'))
COUNTRY = QIcon(os.path.join(IMAGES_ROUTE, 'country-2.svg'))
PROVINCIAS = QIcon(os.path.join(IMAGES_ROUTE, 'flag-1.svg'))
MUNICIPIOS = QIcon(os.path.join(IMAGES_ROUTE, 'location.svg'))
MATERIALS = QIcon(os.path.join(IMAGES_ROUTE, 'materials.svg'))
TECNICAS = QIcon(os.path.join(IMAGES_ROUTE, 'solution.svg'))
TONOS = QIcon(os.path.join(IMAGES_ROUTE, 'palette.svg'))
PAGOS = QIcon(os.path.join(IMAGES_ROUTE, 'credit-card.svg'))
STATS = QIcon(os.path.join(IMAGES_ROUTE, 'stats.svg'))
PRODUCTOS = QIcon(os.path.join(IMAGES_ROUTE, 'products.svg'))
USER = QIcon(os.path.join(IMAGES_ROUTE, 'user.svg'))
ADD_CLIENT = QIcon(os.path.join(IMAGES_ROUTE, 'add-client.svg'))
REFRESH = QIcon(os.path.join(IMAGES_ROUTE, 'refresh.svg'))
BACK_ARROW = QIcon(os.path.join(IMAGES_ROUTE, 'back-arrow.svg'))
UPLOAD_PICTURE = QIcon(os.path.join(IMAGES_ROUTE, 'upload-picture.svg'))
CHANGE_PAGE = QIcon(os.path.join(IMAGES_ROUTE, 'change (2).svg'))
COUNTRY_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'country - white.svg'))
SOCIAL_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'social-network - white.svg'))
EYE = QIcon(os.path.join(IMAGES_ROUTE, 'eye.svg'))
MINIMIZE_DARK = QIcon(os.path.join(IMAGES_ROUTE, 'minimize-dark.svg'))
PLUS = QIcon(os.path.join(IMAGES_ROUTE, 'icons8-plus-24.svg'))
MATERIALS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'materials white.svg'))
MATERIALS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'materials white.svg'))
MUNICIPIOS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'location white.svg'))
PAGOS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'credit-card white.svg'))
PRODUCTOS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'products-white.svg'))
PROVINCIAS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'flag-1 white.svg'))
PROVINCIAS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'flag-1 white.svg'))
PROVINCIAS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'flag-1 white.svg'))
PROVINCIAS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'flag-1 white.svg'))
TECNICAS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'solution white.svg'))
TIPOS_TRABAJOS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'folder-won white.svg'))
TONOS_WHITE = QIcon(os.path.join(IMAGES_ROUTE, 'palette white.svg'))
TIPOS_TRABAJOS = QIcon(os.path.join(IMAGES_ROUTE, 'folder-won.svg'))