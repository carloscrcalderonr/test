from datetime import datetime, date
from sqlalchemy import func
from fastapi import APIRouter

from db.database import Database
from models.contact import DatosDeContactoUpdateRequest, DatosDeContactoRequest
from models.models import DatosDeContacto, Ciudad, Departamento, Pais
from models.response import Response
from sqlalchemy import and_, desc, func

router = APIRouter(
    prefix="/contact",
    tags=["contact"],
    responses={404: {"description": "No encontrado"}},
)

database = Database()
engine = database.get_db_connection()


@router.post("/add", response_description="Registrar Contacto")
async def add_contact(contact_req: DatosDeContactoRequest):
    session = database.get_db_session(engine)
    city_count = session.query(func.count(DatosDeContacto.id)).filter(
        DatosDeContacto.ciudad_id == contact_req.ciudad_id
    ).scalar()

    if city_count >= 3:
        return Response(None, 400, "Cannot add more contacts for this city.", False)
    fecha_nacimiento = datetime.strptime(contact_req.fecha_nacimiento, '%Y-%m-%d').date()
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    if edad < 18:
        return Response(None, 400, "Contact must be at least 18 years old.", False)

    new_contact = DatosDeContacto()
    new_contact.sexo = contact_req.sexo
    new_contact.fecha_nacimiento = contact_req.fecha_nacimiento
    new_contact.nombre = contact_req.nombre
    new_contact.apellido = contact_req.apellido
    new_contact.email = contact_req.email
    new_contact.direccion = contact_req.direccion
    new_contact.casa_apartamento = contact_req.casa_apartamento
    new_contact.ciudad_id = contact_req.ciudad_id
    new_contact.departamento_trabajo = contact_req.departamento_trabajo
    # new_contact.id = None
    print(new_contact)
    session = database.get_db_session(engine)
    session.add(new_contact)
    session.flush()
    session.refresh(new_contact, attribute_names=['id'])
    data = {"contact": new_contact.id}
    session.commit()
    session.close()
    return Response(data, 200, "Save Contact.", False)


@router.put("/update")
async def update_contact(contact_update_req: DatosDeContactoUpdateRequest):
    contact_id = contact_update_req.datos_de_contacto_id
    session = database.get_db_session(engine)
    try:
        is_contact_updated = session.query(DatosDeContacto).filter(DatosDeContacto.id == contact_id).update({
            DatosDeContacto.sexo: contact_update_req.sexo,
            DatosDeContacto.fecha_nacimiento: contact_update_req.fecha_nacimiento,
            DatosDeContacto.nombre: contact_update_req.nombre,
            DatosDeContacto.apellido: contact_update_req.apellido,
            DatosDeContacto.email: contact_update_req.email,
            DatosDeContacto.direccion: contact_update_req.direccion,
            DatosDeContacto.casa_apartamento: contact_update_req.casa_apartamento,
            DatosDeContacto.ciudad_id: contact_update_req.ciudad_id,
            DatosDeContacto.departamento_trabajo: contact_update_req.departamento_trabajo

        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Contact updated successfully"
        response_code = 200
        error = False
        if is_contact_updated == 1:
            # After successful update, retrieve updated data from db
            data = session.query(DatosDeContacto).filter(
                DatosDeContacto.id == contact_id).one()

        elif is_contact_updated == 0:
            response_msg = " Error :" + \
                           str(contact_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)


@router.delete("/{contact_id}/delete")
async def delete_contact(contact_id: str):
    session = database.get_db_session(engine)
    try:
        is_product_updated = session.query(DatosDeContacto).filter(
            and_(DatosDeContacto.id == contact_id, DatosDeContacto.deleted == False)).update({
            DatosDeContacto.deleted: True}, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Contact deleted successfully"
        response_code = 200
        error = False
        data = {"product_id": contact_id}
        if is_product_updated == 0:
            response_msg = "Error Delete :" + \
                           str(contact_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)
@router.get("/")
async def get_all_contacts():
    session = database.get_db_session(engine)
    data = session.query(DatosDeContacto).all()
    return Response(data, 200, "All Contacts retrieved successfully.", False)



@router.get("/city")
async def get_all_contacts_city():
    session = database.get_db_session(engine)
    data = session.query(
        Ciudad.nombre,
        func.count(DatosDeContacto.id)
    ).join(DatosDeContacto).group_by(Ciudad.id).all()
    contacts_by_city = [{"ciudad": name, "cantidad": count} for name, count in data]
    return Response(contacts_by_city, 200, "Contacts retrieved successfully by city.", False)

@router.get("/paises")
async def get_all_countries():
    session = database.get_db_session(engine)
    countries = session.query(Pais).all()
    return [{"id": country.id, "nombre": country.nombre} for country in countries]


@router.get("/pais-departamento/")
async def get_departments_by_country(country_id: int):
    session = database.get_db_session(engine)
    departments = session.query(Departamento).join(Pais).filter(Pais.id == country_id).all()
    result = [{"id": department.id, "nombre": department.nombre} for department in departments]
    return result

@router.get("/departamento-ciudad/{departamento_id}")
async def get_cities_by_department(departamento_id: int):
    session = database.get_db_session(engine)
    cities = session.query(Ciudad).filter(Ciudad.departamento_id == departamento_id).all()
    result = [{"id": city.id, "nombre": city.nombre} for city in cities]
    return result
