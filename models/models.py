from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, String, TIMESTAMP, BOOLEAN, ForeignKey, Date

Base = declarative_base()

class Pais(Base):
    __tablename__ = "paises"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)

class Departamento(Base):
    __tablename__ = "departamentos"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    pais_id = Column(INTEGER, ForeignKey('paises.id'), nullable=False)

class Ciudad(Base):
    __tablename__ = "ciudades"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    departamento_id = Column(INTEGER, ForeignKey('departamentos.id'), nullable=False)

class DatosDeContacto(Base):
    __tablename__ = "datos_de_contacto"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    sexo = Column(String(10), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    direccion = Column(String(100), nullable=False)
    casa_apartamento = Column(String(20), nullable=False)
    ciudad_id = Column(INTEGER, ForeignKey('ciudades.id'), nullable=False)
    departamento_trabajo = Column(String(50), nullable=False)
