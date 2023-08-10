from typing import List, Optional
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, Table, Text, UniqueConstraint, text, cast
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from functools import reduce
from datetime import date
from config import Session

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

class Provincias(Base):
    __tablename__ = 'provincias'
    __table_args__ = (
        UniqueConstraint('provincia', name='provUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    provincia = mapped_column(Text, nullable=False)

    municipios: Mapped[List['Municipios']] = relationship('Municipios', uselist=True, back_populates='provincia', cascade='delete, delete-orphan')

class Socials(Base):
    __tablename__ = 'socials'
    __table_args__ = (
        UniqueConstraint('social', name='socialUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    social = mapped_column(Text, nullable=False)

    client: Mapped[List['Clients']] = relationship('Clients', secondary=t_r_clients_socials, back_populates='social')

class Tecnicas(Base):
    __tablename__ = 'tecnicas'
    __table_args__ = (
        UniqueConstraint('tecnica', name='tecnicaUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    tecnica = mapped_column(Text, nullable=False)

    trabajos: Mapped[List['Trabajos']] = relationship('Trabajos', uselist=True, back_populates='tecnica')

class TipoTrabajos(Base):
    __tablename__ = 'tipo_trabajos'
    __table_args__ = (
        UniqueConstraint('tipo', name='tyoeUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    tipo = mapped_column(Text, nullable=False)

    trabajos: Mapped[List['Trabajos']] = relationship('Trabajos', uselist=True, back_populates='tipo_trabajo', cascade='delete, delete-orphan')
    turnos: Mapped[List['Turnos']] = relationship('Turnos', uselist=True, back_populates='tipo_trabajo' , cascade='delete, delete-orphan')

class TiposPagos(Base):
    __tablename__ = 'tipos_pagos'
    __table_args__ = (
        UniqueConstraint('tipo', name='typeUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    tipo = mapped_column(Text, nullable=False)

    trabajos: Mapped[List['Trabajos']] = relationship('Trabajos', uselist=True, back_populates='tipo_pago')
    turnos: Mapped[List['Turnos']] = relationship('Turnos', uselist=True, back_populates='tipo_pago')

class Tonalidades(Base):
    __tablename__ = 'tonalidades'
    __table_args__ = (
        UniqueConstraint('tono', name='tonoUnique'),
    )

    id = mapped_column(Integer, primary_key=True)
    tono = mapped_column(Text, nullable=False)

    trabajos: Mapped[List['Trabajos']] = relationship('Trabajos', uselist=True, back_populates='tonalidad')

class Municipios(Base):
    __tablename__ = 'municipios'
    __table_args__ = (
        UniqueConstraint('municipio', name='municipio'),
    )

    id = mapped_column(Integer, primary_key=True)
    municipio = mapped_column(Text, nullable=False)
    provincia_id = mapped_column(ForeignKey('provincias.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    provincia: Mapped['Provincias'] = relationship('Provincias', back_populates='municipios', )
    clients: Mapped[List['Clients']] = relationship('Clients', uselist=True, back_populates='municipio',cascade='delete, delete-orphan')

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
    pais_id = mapped_column(ForeignKey('paises.id', ondelete='SET NULL', onupdate='CASCADE'), server_default='1')

    municipio: Mapped[Optional['Municipios']] = relationship('Municipios', back_populates='clients')
    trabajos: Mapped[List['Trabajos']] = relationship('Trabajos', uselist=True, back_populates='cliente',  cascade='delete, delete-orphan', order_by="desc(Trabajos.created_at)")
    turnos: Mapped[List['Turnos']] = relationship('Turnos', uselist=True, back_populates='cliente', cascade='delete, delete-orphan')
    social: Mapped[List['Socials']] = relationship('Socials', secondary=t_r_clients_socials, back_populates='client')
    pais: Mapped[Optional['Paises']] = relationship('Paises', back_populates='clients')
    
    def gastos(self)->float:
        if self.trabajos:
            return reduce(lambda x,y: x + y, map(lambda x: x.price, self.trabajos))
        else:
            return 0
        
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

class Paises(Base):
    __tablename__ = 'paises'

    id = mapped_column(Integer, primary_key=True)
    pais = mapped_column(Text, nullable=False)

    clients: Mapped[List['Clients']] = relationship('Clients', uselist=True, back_populates='pais')
