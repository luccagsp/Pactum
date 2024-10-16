from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for
from models import Availability, Eventhall
from auth_service import AuthService
from config.objToStr import objToStr
from config.validateHours import validate_json_hours_structure
from db import db
from upload import query_image

eventhall = Blueprint('eventhall', __name__)

@eventhall.route('/eventhall/<id>', methods=["GET"])
def query_salon(id):
    eventhall = Eventhall.query.filter_by(id=id).first()
    if not eventhall:
        return ["Error: Event hall not found"]
    return {'id' : eventhall.id, 'nombre' : eventhall.nombre, 'descripcion' : eventhall.descripcion, 'calle_domicilio' : eventhall.calle_domicilio, 'numero_domicilio' : eventhall.numero_domicilio, 'email_contacto' : eventhall.email_contacto, 'telefono_contacto' : eventhall.telefono_contacto, 'precio_sena' : eventhall.precio_sena, 'imagenes' : eventhall.imagenes, 'reserva_instantanea' : eventhall.reserva_instantanea, 'creado_en' : eventhall.creado_en, 'actualizado_en' : eventhall.actualizado_en} 

@eventhall.route('/register/eventhall', methods=["GET", "POST"])
@login_required
def create_eventhall():
    if request.method == 'GET':
        return render_template('register_eventhall.html', user=current_user)
    #POST:
    data = request.form.to_dict(flat=True)
    print(data)
    image = request.files["file"]
    if not image:
        return "Falta 'file'"
    
    login_user_dto = Eventhall.validate_eventhall(owner_id=current_user.id, **data)
    if login_user_dto[0] == False:
        flash(login_user_dto[1], category='error')
        return render_template('register_eventhall.html', user=current_user)
    eventhall = login_user_dto[0]
    AuthService.create_eventhall(eventhall, image)
    flash('Salón creado exitosamente', category='success')
    return render_template('register_eventhall.html', user=current_user)


# @auth.route('/register/eventhall', methods=["GET", "POST"])
# @login_required
# def register_eventhall():
#     data = request.get_json()
#     userId = current_user.id
#     validate_hall_dto = Eventhall.validate_eventhall(**data, owner=userId)
#     if validate_hall_dto[0] != None:
#         return validate_hall_dto
#     eventhall = validate_hall_dto[1]
#     print(userId, eventhall)
#     AuthService.create_eventhall(eventhall)

#     return render_template("index.html")




@eventhall.route('/update/eventhall', methods=["GET", "POST"])
@login_required
def edit_eventhall():
    if request.method == "GET":
        return render_template("put_eventhall.html", user=current_user)
    #POST:
    data = request.form.to_dict(flat=True)
    print(data)
    print("asdad")
    id = request.form["eventhallId"]

    eventhall = Eventhall.query.filter_by(id=id).first()  

    if not eventhall:
        flash(f"Event hall with ID '{id}' not found", category='error')
        return redirect(url_for('eventhall.edit_eventhall'))
    if "owner_id" in data and eventhall.owner != data.get("owner"):
        flash("No se puede cambiar de dueño", category='error')
        return redirect(url_for('eventhall.edit_eventhall'))
    if current_user.id != eventhall.owner_id:
        flash(f"Solo se pueden cambiar tus salones", category='error')
        return redirect(url_for('eventhall.edit_eventhall'))
    print(data)
    for column in data:
        setattr(eventhall, column, data[column]) # Actualiza eventhall
    destructured_eventhall = objToStr(eventhall)
    destructured_eventhall.pop('id', None)
    destructured_eventhall.pop('updated_at', None)
    destructured_eventhall.pop('created_at', None)
    destructured_eventhall.pop('eventhallId', None)
    eventhall.description = destructured_eventhall['description']
    dto = Eventhall.validate_eventhall(**destructured_eventhall)
    if dto[0] != False:
        db.session.commit()
    else:
        flash(dto[1], category='error')
        return redirect(url_for('eventhall.edit_eventhall'))
    flash('Descripcion cabiada exitosamente', category='success')
    return redirect(url_for('eventhall.edit_eventhall'))
@eventhall.route('/eventhall/<id>/addAvailability', methods=["POST"])
@login_required
def add_availability(id):
    data = request.get_json()
    checkedData = validate_json_hours_structure(data)
    if checkedData[0] == False: #Si el verificador retorna 'False'
        flash(checkedData[1])
        return(checkedData[1]) 
    availabilityExists = Availability.query.filter_by(eventhall_id=id).first()
    if availabilityExists:
        return [f"Error: Availability for Event hall with id '{id}' already exists"]
    eventhall = Eventhall.query.filter_by(id=id).first()
    if current_user.id != eventhall.owner_id:
        return f"Error: Only event hall owners can change Availability"
    flash(f"Successfully added Availability to Event Hall: '{eventhall.name}'", category='success')
    availability = Availability(eventhall_id=id, hours=data)
    db.session.add(availability)
    db.session.commit()

    print(objToStr(availability))
    return objToStr(availability)