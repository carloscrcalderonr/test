import re

from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional



class Pais(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True


class Departamento(BaseModel):
    id: int
    nombre: str
    pais_id: int

    class Config:
        orm_mode = True


class Ciudad(BaseModel):
    id: int
    nombre: str
    departamento_id: int

    class Config:
        orm_mode = True


class DatosDeContactoRequest(BaseModel):
    sexo: Optional[str]
    fecha_nacimiento: Optional[str]
    nombre: Optional[str]
    apellido: Optional[str]
    email: Optional[str]
    direccion: Optional[str]
    casa_apartamento: Optional[str]
    ciudad_id: Optional[int]
    departamento_trabajo: Optional[str]

    @validator('sexo')
    def validate_sexo(cls, value):
        if value not in ['f', 'm']:
            raise ValueError('El sexo debe ser "f" o "m"')
        return value

    @validator('nombre', 'apellido')
    def validate_nombre_apellido(cls, value):
        if any(char.isdigit() for char in value):
            raise ValueError('Los nombres y apellidos no deben contener números')
        return value

    @validator('email')
    def validate_email(cls, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError('El email no es válido')
        return value
class DatosDeContactoUpdateRequest(BaseModel):
    datos_de_contacto_id: int
    sexo: str
    fecha_nacimiento: str
    nombre: str
    apellido: str
    email: str
    direccion: str
    casa_apartamento: str
    ciudad_id: int
    departamento_trabajo: str
