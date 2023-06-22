from PyQt6.QtCore import QDate



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