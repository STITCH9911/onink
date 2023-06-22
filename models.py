from typing import List, Optional, Tuple
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, Table, Text, UniqueConstraint, text, or_
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from config import Session
from PyQt6.QtCore import QDate

Base = declarative_base()
metadata = Base.metadata

t_r_trabajos_materiales = Table(
    'r_trabajos_materiales', metadata,
    Column('trabajo_id', ForeignKey('trabajos.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('material_id', ForeignKey('materiales.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
)


t_r_clients_socials = Table(
    'r_clients_socials', metadata,
    Column('username', Text, nullable=False),
    Column('client_id', ForeignKey('clients.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('social_id', ForeignKey('socials.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
)


class Materiales(Base):
    __tablename__ = 'materiales'
    __table_args__ = (
        UniqueConstraint('material', name='materialUnique'),
    )
    id = mapped_column(Integer, primary_key=True)
    material = mapped_column(Text, nullable=False)
    costo = mapped_column(Float)

    trabajo: Mapped[List['Trabajos']] = relationship('Trabajos', secondary=t_r_trabajos_materiales, back_populates='material')

    @staticmethod
    def getByCriterion(**arg) -> Tuple['Materiales']:
        lista = []

        if "search" in arg:
            try:
                float(arg["search"])
                with Session() as session:
                    q = session.query(Materiales).filter(Materiales.costo.like(f"%{arg['search']}%")).all()
                    lista += q
            except ValueError:
                pass
            finally:
                with Session() as session:
                    q = session.query(Materiales).filter(Materiales.material.like(f"%{arg['search']}%")).all()
                    lista += q

        res = set(lista)
        return tuple(res)


class Provincias(Base):
    __tablename__ = 'provincias'
    __table_args__ = (
        UniqueConstraint('provincia', name='provUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    provincia = mapped_column(Text, nullable=False)

    municipios: Mapped[List['Municipios']] = relationship('Municipios', uselist=True, back_populates='provincia')

    @staticmethod
    def getByCriterion(**arg) -> Tuple['Provincias']:
        lista = []

        if "search" in arg:
           with Session() as session:
               q = session.query(Provincias).filter(Provincias.provincia.like(f"%{arg['search']}%")).all()
               lista += q
        res = set(lista)
        return tuple(res)

class Socials(Base):
    __tablename__ = 'socials'
    __table_args__ = (
        UniqueConstraint('social', name='socialUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    social = mapped_column(Text, nullable=False)

    client: Mapped[List['Clients']] = relationship('Clients', secondary=t_r_clients_socials, back_populates='social')

    @staticmethod
    def getByCriterion(**arg) -> Tuple['Socials']:
        lista = []

        if "search" in arg:
            with Session() as session:
                q = session.query(Socials).filter(Socials.social.like(f"%{arg['search']}%")).all()
                lista += q
                    
        res = set(lista)
        return tuple(res)

class Tecnicas(Base):
    __tablename__ = 'tecnicas'
    __table_args__ = (
        UniqueConstraint('tecnica', name='tecnicaUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    tecnica = mapped_column(Text, nullable=False)

    trabajos: Mapped[List['Trabajos']] = relationship('Trabajos', uselist=True, back_populates='tecnica')

    @staticmethod
    def getByCriterion(**arg) -> Tuple['Tecnicas']:
        lista = []

        if "search" in arg:
            with Session() as session:
                q = session.query(Tecnicas).filter(Tecnicas.tecnica.like(f"%{arg['search']}%")).all()
                lista += q

        res = set(lista)
        return tuple(res)


class TipoTrabajos(Base):
    __tablename__ = 'tipo_trabajos'
    __table_args__ = (
        UniqueConstraint('tipo', name='tyoeUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    tipo = mapped_column(Text, nullable=False)

    trabajos: Mapped[List['Trabajos']] = relationship('Trabajos', uselist=True, back_populates='tipo_trabajo')
    turnos: Mapped[List['Turnos']] = relationship('Turnos', uselist=True, back_populates='tipo_trabajo')

    @staticmethod
    def getByCriterion(**arg) -> Tuple['TipoTrabajos']:
         lista = []

         if "search" in arg:
            with Session() as session:
                q = session.query(TipoTrabajos).filter(TipoTrabajos.tipo.like(f"%{arg['search']}%")).all()
                lista += q

         res = set(lista)
         return tuple(res)


class TiposPagos(Base):
    __tablename__ = 'tipos_pagos'
    __table_args__ = (
        UniqueConstraint('tipo', name='typeUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    tipo = mapped_column(Text, nullable=False)

    trabajos: Mapped[List['Trabajos']] = relationship('Trabajos', uselist=True, back_populates='tipo_pago')
    turnos: Mapped[List['Turnos']] = relationship('Turnos', uselist=True, back_populates='tipo_pago')

    @staticmethod
    def getByCriterion(**arg):
        lista = []

        if "search" in arg:
            with Session() as session:
                q = session.query(TiposPagos).filter(TiposPagos.tipo.like(f"%{arg['search']}%")).all()
                lista += q

        res = set(lista)
        return tuple(res)


class Tonalidades(Base):
    __tablename__ = 'tonalidades'
    __table_args__ = (
        UniqueConstraint('tono', name='tonoUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    tono = mapped_column(Text, nullable=False)

    trabajos: Mapped[List['Trabajos']] = relationship('Trabajos', uselist=True, back_populates='tonalidad')

    @staticmethod
    def getByCriterion(**arg) -> Tuple['Tonalidades']:
        lista = []

        if "search" in arg:
            with Session() as session:
                q = session.query(Tonalidades).filter(Tonalidades.tono.like(f"%{arg['search']}%")).all()
                lista += q

        res = set(lista)
        return tuple(res)


class Municipios(Base):
    __tablename__ = 'municipios'
    __table_args__ = (
        UniqueConstraint('municipio', name='municipio'),
    )

    id = mapped_column(Integer, primary_key=True)
    municipio = mapped_column(Text, nullable=False)
    provincia_id = mapped_column(ForeignKey('provincias.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    provincia: Mapped['Provincias'] = relationship('Provincias', back_populates='municipios')
    clients: Mapped[List['Clients']] = relationship('Clients', uselist=True, back_populates='municipio')

    @staticmethod
    def getByCriterion(**arg):
        lista = []

        if "search" in arg:
            with Session() as session:
                q = session.query(Municipios).filter(Municipios.municipio.like(f"%{arg['search']}%")).all()
                lista += q

        r = set(lista)
        return tuple(r)


class Clients(Base):
    __tablename__ = 'clients'
    __table_args__ = (
        UniqueConstraint('ci', name='uniqueCi'),
    )

    id = mapped_column(Integer, primary_key=True)
    nombre_apellidos = mapped_column(Text(255), nullable=False)
    direccion = mapped_column(Text(255))
    ci = mapped_column(Text, nullable=False)
    notes = mapped_column(Text)
    created_at = mapped_column(DateTime, nullable=False)
    phone = mapped_column(Text)
    alcance = mapped_column(Text)
    municipio_id = mapped_column(ForeignKey('municipios.id', ondelete='SET NULL', onupdate='CASCADE'))
    pais_id = mapped_column(ForeignKey('paises.id', ondelete='SET NULL', onupdate='CASCADE'))

    municipio: Mapped[Optional['Municipios']] = relationship('Municipios', back_populates='clients')
    trabajos: Mapped[List['Trabajos']] = relationship('Trabajos', uselist=True, back_populates='cliente')
    turnos: Mapped[List['Turnos']] = relationship('Turnos', uselist=True, back_populates='cliente')
    social: Mapped[List['Socials']] = relationship('Socials', secondary=t_r_clients_socials, back_populates='client')
    pais: Mapped[List['Paises']] = relationship('Paises', uselist=True, back_populates='clients')

    
    @staticmethod
    def getByCriterion(**arg) -> Tuple['Clients']:
        lista = [] #lista de resultados
        switcher = {
            "municipio_id": Clients.getByMunicipioId,
            "provincia_id": Clients.getByProvinciaId,
            "pais_id": Clients.getByPaisId,
        }
        for llave in arg:
            if llave in switcher:
                funcion = switcher.get(llave)
                lista.extend(funcion(arg[llave]))
        if "search" in arg:
            try:
                int(arg["search"]) #evalua si el argumento es un numero o no
                #si es numero usa estos filtros
                with Session() as session:
                    q1 = session.query(Clients).filter(Clients.ci.like(f"%{arg['search']}%")).all() #filtro por ci
                    q2 = session.query(Clients).filter(Clients.phone.like(f"%{arg['search']}%")).all() #filtro por telefono
                    lista = q1 + q2 #agregar resultados a la lista
            except ValueError:
                with Session() as session:
                    q1 = session.query(Clients).filter(Clients.nombre_apellidos.like(f"%{arg['search']}%")).all() # filtro por nombre y apellidos
                    q2 = session.query(Clients).join(t_r_clients_socials).filter(t_r_clients_socials.c.username.like(f"%{arg['search']}%")).all()
                    lista = q1 + q2
            with Session() as session:
                q = session.query(Clients).filter(Clients.direccion.like(f"%{arg['search']}%")).all() #filtro por direccion
                lista += q
        lista = set(lista)
        res = tuple(lista)
        return res
    
    @staticmethod
    def getByMunicipioId(id) -> Optional[List['Clients']]:
        with Session() as session:
            q = session.query(Clients).filter_by(municipio_id=id).all()
        return q

    @staticmethod
    def getByProvinciaId(id) -> Optional[List['Clients']]:
        with Session() as session:
            q = session.query(Clients).join(Municipios).join(Provincias).filter(Provincias.id == id).all()
        return q
    
    @staticmethod
    def getByPaisId(id):
        with Session() as session:
            q = session.query(Clients).filter_by(pais_id=id).all()
        return q
    

class Trabajos(Base):
    __tablename__ = 'trabajos'

    id = mapped_column(Integer, primary_key=True)
    cliente_id = mapped_column(ForeignKey('clients.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    tipo_trabajo_id = mapped_column(ForeignKey('tipo_trabajos.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    tipo_pago_id = mapped_column(ForeignKey('tipos_pagos.id', ondelete='SET NULL', onupdate='SET NULL'))
    created_at = mapped_column(DateTime)
    tonalidad_id = mapped_column(ForeignKey('tonalidades.id', ondelete='SET NULL', onupdate='SET NULL'))
    tecnica_id = mapped_column(ForeignKey('tecnicas.id', ondelete='SET NULL', onupdate='SET NULL'))
    price = mapped_column(Float)
    fecha_pago = mapped_column(Date)

    material: Mapped[List['Materiales']] = relationship('Materiales', secondary=t_r_trabajos_materiales, back_populates='trabajo')
    cliente: Mapped['Clients'] = relationship('Clients', back_populates='trabajos')
    tecnica: Mapped[Optional['Tecnicas']] = relationship('Tecnicas', back_populates='trabajos')
    tipo_pago: Mapped[Optional['TiposPagos']] = relationship('TiposPagos', back_populates='trabajos')
    tipo_trabajo: Mapped['TipoTrabajos'] = relationship('TipoTrabajos', back_populates='trabajos')
    tonalidad: Mapped[Optional['Tonalidades']] = relationship('Tonalidades', back_populates='trabajos')
    turnos: Mapped[List['Turnos']] = relationship('Turnos', uselist=True, back_populates='trabajo')

    @staticmethod
    def getByCriterion(**arg) -> Tuple['Trabajos']:
        lista = []
        switcher = {
            'cliente_id': Trabajos.getByCliente,
            'tipo_trabajo_id': Trabajos.getByTipoTrabajo,
            'tipo_pago_id': Trabajos.getByTipoPago,
            'tonalidad_id': Trabajos.getByTonalidad,
            'tecnica_id' : Trabajos.getByTecnica
        }
        for llave in arg:
            if llave in switcher:
                funcion = switcher[llave]
                lista += funcion(arg[llave])

        if 'search' in arg:
            fecha = arg['search']
            if isinstance(fecha, QDate):
                fecha = fecha.toString("yyyy-mm-dd")
                with Session() as session:
                    q = session.query(Trabajos).filter(or_(Trabajos.created_at.like(f"%{fecha}%"), Trabajos.fecha_pago == fecha)).all()
                    lista += q
        res = set(lista)
        return tuple(res)
    
    @staticmethod
    def getByCliente(id) -> Tuple['Trabajos']:
        lista = []
        with Session() as session:
            q = session.query(Trabajos).filter_by(cliente_id = id).all()
            lista += q
        res = set(lista)
        return tuple(res)
    
    @staticmethod
    def getByTipoTrabajo(id) -> Tuple['Trabajos']:
        lista = []
        with Session() as session:
            q = session.query(Trabajos).filter_by(tipo_trabajo_id = id).all()
            lista += q
        res = set(lista)
        return tuple(res)
    
    @staticmethod
    def getByTipoPago(id) -> Tuple['Trabajos']:
        lista = []
        with Session() as session:
            q = session.query(Trabajos).filter_by(tipo_pago_id = id).all()
            lista += q
        res = set(lista)
        return tuple(res)
    
    @staticmethod
    def getByTonalidad(id) -> Tuple['Trabajos']:
        lista = []
        with Session() as session:
            q = session.query(Trabajos).filter_by(tonalidad_id = id).all()
            lista += q
        res = set(lista)
        return tuple(res)

    @staticmethod
    def getByTecnica(id) -> Tuple['Trabajos']:
        lista = []
        with Session() as session:
            q = session.query(Trabajos).filter_by(tecnica_id = id).all()
            lista += q
        res = set(lista)
        return tuple(res)


class Turnos(Base):
    __tablename__ = 'turnos'

    id = mapped_column(Integer, primary_key=True)
    cliente_id = mapped_column(ForeignKey('clients.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    fecha = mapped_column(DateTime, nullable=False)
    created_at = mapped_column(DateTime, nullable=False)
    tipo_trabajo_id = mapped_column(ForeignKey('tipo_trabajos.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    deposito = mapped_column(Float, server_default=text('0'))
    deposito_fecha = mapped_column(Date)
    tipo_pago_id = mapped_column(ForeignKey('tipos_pagos.id', ondelete='SET NULL', onupdate='SET NULL'))
    trabajo_id = mapped_column(ForeignKey('trabajos.id', ondelete='SET NULL', onupdate='SET NULL'))

    cliente: Mapped['Clients'] = relationship('Clients', back_populates='turnos')
    tipo_pago: Mapped[Optional['TiposPagos']] = relationship('TiposPagos', back_populates='turnos')
    tipo_trabajo: Mapped['TipoTrabajos'] = relationship('TipoTrabajos', back_populates='turnos')
    trabajo: Mapped[Optional['Trabajos']] = relationship('Trabajos', back_populates='turnos')

    @staticmethod
    def getByCriterion(**arg) -> Tuple['Turnos']:
        lista = []

        switcher = {
            'cliente_id': Turnos.getByCliente,
            'tipo_trabajo_id': Turnos.getByTipoTrabajo,
            'tipo_pago_id': Turnos.getByTipoPago,
            'trabajo_id': Turnos.getByTrabajo,
        }

        for llave in arg:
            if llave in switcher:
                funcion = switcher[arg[llave]]
                q = funcion(arg[llave])
                lista += q
        
        if 'search' in arg:
            with Session() as session:
                search = arg['search']
                try:
                    float(search)
                    q = session.query(Turnos).filter(Turnos.deposito.like(f"%{search}%")).all()
                    lista += q
                except ValueError:
                    if isinstance(search, QDate):
                        fecha = search.toString("yyyy-mm-dd")
                        q = session.query(Turnos).filter(or_(Turnos.created_at.like(f"%{fecha}%"), Turnos.deposito_fecha == fecha, Turnos.fecha.like(f"%{fecha}%"))).all()
                        lista += q

        res = set(lista)
        return tuple(res)
    
    @staticmethod
    def getByCliente(id) -> Tuple['Turnos']:
        lista = []
        with Session() as session:
            q = session.query(Turnos).filter_by(cliente_id=id).all()
            lista += q
        
        res = set(lista)
        return tuple(res)
    
    @staticmethod
    def getByTipoTrabajo(id) -> Tuple['Turnos']:
        lista = []
        with Session() as session:
            q = session.query(Turnos).filter_by(tipo_trabajo_id=id).all()
            lista += q
        
        res = set(lista)
        return tuple(res)
    
    @staticmethod
    def getByTipoPago(id) -> Tuple['Turnos']:
        lista = []
        with Session() as session:
            q = session.query(Turnos).filter_by(tipo_pago_id=id).all()
            lista += q
        
        res = set(lista)
        return tuple(res)
    @staticmethod
    def getByTrabajo(id) -> Tuple['Turnos']:
        lista = []
        with Session() as session:
            q = session.query(Turnos).filter_by(trabajo_id=id).all()
            lista += q
        
        res = set(lista)
        return tuple(res)


class Paises(Base):
    __tablename__ = 'paises'

    id = mapped_column(Integer, primary_key=True)
    pais = mapped_column(Text, nullable=False)

    clients: Mapped[List['Clients']] = relationship('Clients', uselist=True, back_populates='pais')

    @staticmethod
    def getByCriterion(**arg):
        lista = []

        if "search" in arg:
            with Session() as session:
                q = session.query(Paises).filter(Paises.pais.like(f"%{arg['search']}%")).all()
                lista += q

        r = set(lista)
        return tuple(r)
