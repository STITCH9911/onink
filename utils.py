from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QIcon
from datetime import datetime
import os

from models import Clients

def is_cumpleannos(client: Clients)->bool:
    hoy = datetime.now().strftime('%m%d')
    birthday = str(client.ci)[2:6]
    return hoy == birthday

def get_birthday(ci: str) -> QDate:
    fecha_str = ci[:6]
    year = int(fecha_str[:2])
    hoy = QDate.currentDate()

    yearActual = hoy.year() - 2000
    if year <= yearActual:
        year = year+2000
    else:
        year = year + 1900
    
    month = int(fecha_str[2:4])
    day = int(fecha_str[4:6])

    fecha = QDate(year,month,day)

    return fecha

def get_age(ci):
    fecha_nacimiento = get_birthday(ci=str(ci))
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

#metodo para aeliminar ocntenido de un layout
def eliminar_contenido(contenedor):
    while contenedor.count():
        item = contenedor.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
        else:
            sublayout = item.layout()
            if sublayout is not None:
                eliminar_contenido(sublayout)
            contenedor.removeItem(item)

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
INVERT = QIcon(os.path.join(IMAGES_ROUTE,'change (3).svg'))
BIRTHDAY = QIcon(os.path.join(IMAGES_ROUTE, 'birthday (3).svg'))