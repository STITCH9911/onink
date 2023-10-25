from faker import Faker
from models import Materiales, Provincias, Socials, Tecnicas, TipoTrabajos, TiposPagos, Tonalidades, Municipios, Clients, Trabajos, Turnos, Paises, t_r_clients_socials, Base
from sqlalchemy import insert
import random
from datetime import date
from config import set_config, Session, engine

fake  = Faker()
def crear():
    materiales, provincias, socials, tecnicas, tipo_trabajos, tipo_pagos, tonalidades, municipios, clientes, trabajos, turnos, paises = [], [], [], [], [], [], [], [], [], [], [], []

    material = fake.words(unique=True, nb=5)
    costos = [fake.random_number(digits=2) for _ in range(5)]
    provincia = fake.words(unique=True, nb=5)
    scls = fake.words(unique=True, nb=5)
    tecnique = fake.words(unique=True, nb=5)
    types_trb = fake.words(unique=True, nb=5)
    types_pay = fake.words(unique=True, nb=5)
    tonalities = fake.words(unique=True, nb=5)
    municipio = fake.words(unique=True, nb=5)
    cis = random.sample([fake.random_number(digits=11) for _ in range(100)], 5)
    direcciones = [fake.address() for _ in range(5)]
    notas = [fake.paragraph() for _ in range(5)]
    creados = [fake.date_time() for _ in range(5)]
    telefonos = [fake.phone_number() for _ in range(5)]
    alcances = [fake.paragraph() for _ in range(5)]
    pais = ['Cuba', 'USA', 'Canada', 'Venezuela', 'Argentina']
    
    for i in range(4):
        p = pais[i]
        obj = Paises(pais=p)
        paises.append(obj)

    for i in range(5):
        m = material[i]
        c = costos[i]
        p = provincia[i]
        s = scls[i]
        tqni = tecnique[i]
        tt = types_trb[i]
        tp = types_pay[i]
        ton = tonalities[i]

        materialobj = Materiales(material=m, costo=c)
        provincia_obj = Provincias(provincia=p)
        social_obj = Socials(social=s)
        tecniques_obj = Tecnicas(tecnica=tqni)
        type_trabajos_obj = TipoTrabajos(tipo=tt)
        type_pagos_obj = TiposPagos(tipo=tp)
        tonalidad_obj = Tonalidades(tono=ton)

        materiales.append(materialobj)
        provincias.append(provincia_obj)
        socials.append(social_obj)
        tecnicas.append(tecniques_obj)
        tipo_trabajos.append(type_trabajos_obj)
        tipo_pagos.append(type_pagos_obj)
        tonalidades.append(tonalidad_obj)
    

    for i in range(5):
        m = municipio[i]
        municipio_obj = Municipios(municipio=m)
        municipio_obj.provincia = fake.random_element(provincias)
        municipios.append(municipio_obj)

    for i in range(5):
        ci = cis[i]
        dir = direcciones[i]
        n = notas[i]
        c_at = creados[i]
        t = telefonos[i]
        alc = alcances[i]

        client_obj = Clients(direccion=dir, ci=ci, notes= n, created_at= c_at, phone=t, alcance=alc)
        client_obj.nombre_apellidos = fake.name()
        client_obj.municipio = fake.random_element(municipios)
        clientes.append(client_obj)


    for i in range(5):
        c_at = creados[i]
        p = fake.random_number(digits=4)
        f_p = date.fromisoformat(fake.date())

        trabajo_obj = Trabajos(created_at=c_at, price=p, fecha_pago=f_p)
        trabajo_obj.cliente = fake.random_element(clientes)
        trabajo_obj.tecnica = fake.random_element(tecnicas)
        trabajo_obj.tipo_pago = fake.random_element(tipo_pagos)
        trabajo_obj.tipo_trabajo = fake.random_element(tipo_trabajos)
        trabajo_obj.tonalidad = fake.random_element(tonalidades)

        trabajos.append(trabajo_obj)

    for i in range(5):
        c_at = fake.date_time()
        f = fake.date_time()
        d = fake.random_element([500,0])
        d_f = date.fromisoformat(fake.date())

        turno_obj = Turnos(created_at=c_at, fecha=f, deposito=d, deposito_fecha=d_f)
        turno_obj.cliente = fake.random_element(clientes)
        turno_obj.tipo_pago = fake.random_element(tipo_pagos)
        turno_obj.tipo_trabajo = fake.random_element(tipo_trabajos)
        turnos.append(turno_obj)

        with Session() as session:
            session.add_all(materiales)
            session.add_all(provincias)
            session.add_all(socials)
            session.add_all(tecnicas)
            session.add_all(tipo_trabajos)
            session.add_all(tipo_pagos)
            session.add_all(tonalidades)
            session.add_all(municipios)
            session.add_all(clientes)
            session.add_all(trabajos)
            session.add_all(turnos)
            session.add_all(paises)
            session.commit()


def relacionar():
    with Session() as session:
        materiales = session.query(Materiales).all()
        socials = session.query(Socials).all()
        clientes = session.query(Clients).all()
        trabajos = session.query(Trabajos).all()

        for client in clientes:
            social_aleatoria = fake.random_elements(elements=socials, unique=True)
            for social in social_aleatoria:
                username = fake.user_name()
                stmp = insert(t_r_clients_socials).values(username=username, client_id=client.id, social_id=social.id)
                session.execute(stmp)

        for trabajo in trabajos:
            material_aleatorio = fake.random_elements(elements=materiales, unique=False)
            if material_aleatorio:
                trabajo.material.extend(material_aleatorio)

        session.commit()

def obtener_datos():
    with Session() as session:
        materiales = session.query(Materiales.material).all()
        socials = session.query(Socials).all()
        clientes = session.query(Clients.nombre_apellidos, Clients.id, t_r_clients_socials.c.username, Socials.social).select_from(Clients).join(t_r_clients_socials).join(Socials).filter(t_r_clients_socials.c.username == "michelebrown").all()
        trabajos = session.query(Trabajos.price, TipoTrabajos.tipo).join(TipoTrabajos).all()
        municipios = session.query(Municipios).all()
        tecnicas = session.query(Tecnicas)
        t_trabajos = session.query(TipoTrabajos)
        t_pagos = session.query(TiposPagos)
        tonalidades = session.query(Tonalidades)
        turnos = session.query(Turnos)
        provincias = session.query(Provincias).all()
        
    return map(lambda item: tuple(map(lambda x: x.nombre_apellidos,item.client)),socials)

def cr_del_wr_db(b, e):
    b.metadata.drop_all(e)
    b.metadata.create_all(e)

def execute_falsos():
    cr_del_wr_db(Base, engine)
    set_config("DATABASE", 'created', True)
    print("Base de datos creada correctamente.")

def funcionClientesMillares():
    clientes = []

    cis = random.sample([fake.random_number(digits=11) for _ in range(1000)], 1000)
    direcciones = [fake.address() for _ in range(1000)]
    notas = [fake.paragraph() for _ in range(1000)]
    creados = [fake.date_time() for _ in range(1000)]
    telefonos = [fake.phone_number() for _ in range(1000)]
    alcances = [fake.paragraph() for _ in range(1000)]

    for i in range(1000):
        ci = cis[i]
        dir = direcciones[i]
        n = notas[i]
        c_at = creados[i]
        t = telefonos[i]
        alc = alcances[i]

        client_obj = Clients(direccion=dir, ci=ci, notes= n, created_at= c_at, phone=t, alcance=alc)
        client_obj.nombre_apellidos = fake.name()
        client_obj.municipio_id = 0
        clientes.append(client_obj)
    
    with Session() as session:
        session.add_all(clientes)
        session.commit()
    
    print("TERMINADO")

def rectificar():
    with Session() as session:
        clients = session.query(Clients).all()
        for c in clients:
            c.municipio_id = 1
        session.add_all(clients)
        session.commit()
    print("Terminado")
if __name__ == "__main__":
    #funcionClientesMillares()
    rectificar()