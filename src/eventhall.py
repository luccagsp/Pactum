from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for
from models import Availability, Eventhall
from auth_service import AuthService
from config.objToStr import objToStr
from db import db
eventhall = Blueprint('eventhall', __name__)

@eventhall.route('/')
@eventhall.route('/eventhall/<id>', methods=["GET"])
def query_salon(id):
    eventhall = Eventhall.query.filter_by(id=id).first()
    if not eventhall:
        return ["Error: Event hall not found"]
    return {'id' : eventhall.id, 'nombre' : eventhall.nombre, 'descripcion' : eventhall.descripcion, 'calle_domicilio' : eventhall.calle_domicilio, 'numero_domicilio' : eventhall.numero_domicilio, 'email_contacto' : eventhall.email_contacto, 'telefono_contacto' : eventhall.telefono_contacto, 'precio_sena' : eventhall.precio_sena, 'imagenes' : eventhall.imagenes, 'reserva_instantanea' : eventhall.reserva_instantanea, 'creado_en' : eventhall.creado_en, 'actualizado_en' : eventhall.actualizado_en} 

@eventhall.route('/eventhall/<id>', methods=["PUT"])
@login_required
def edit_eventhall(id):
    data = request.get_json()
    eventhall = Eventhall.query.filter_by(id=id).first()  
    
    if not eventhall:
        return[f"Event hall with ID '{id}' not found"]
    if "owner" in data and eventhall.owner != data.get("owner"):
        return["No se puede cambiar de dueño, flaco, picá de acá"]
    if current_user.id != eventhall.owner:
        return ["Este no es tu salón, flaco, picá de acá"]
    
    for column in data:
        setattr(eventhall, column, data[column]) # Actualiza eventhall
    destructured_eventhall = objToStr(eventhall)
    destructured_eventhall.pop('id', None)
    destructured_eventhall.pop('updated_at', None)
    destructured_eventhall.pop('created_at', None)

    if Eventhall.validate_eventhall(**destructured_eventhall)[0] == None:
        db.session.commit()

    return objToStr(eventhall)
@eventhall.route('/eventhall/<id>/addAvailability', methods=["POST"])
@login_required
def add_availability(id):
    data = request.get_json()
    
    availabilityExists = Availability.query.filter_by(eventhall_id=id).first()
    if availabilityExists:
        return [f"Error: Availability for Event hall with id '{id}' already exists"]
    if data[0] == False: #Si el verificador retorna 'False'
        return [f"Error: Invalid hours structure: {data[1]}"]
    
    eventhall = Eventhall.query.filter_by(id=id).first()
    if current_user.id != eventhall.owner_id:
        return f"Error: Only event hall owners can change Availability"
    flash(f"Successfully added Availability to Event Hall: '{eventhall.name}'", category='success')
    availability:Availability = Availability(eventhall_id=id, hours=data)
    db.session.add(availability)
    db.session.commit()

    print(objToStr(availability))
    return objToStr(availability)