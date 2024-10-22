from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for
from models import Availability, Eventhall
from auth_service import AuthService
from config.objToStr import objToStr
from db import db
eventhall = Blueprint('eventhall', __name__)

@eventhall.route('/eventhall_list')
def eventhall_list():
    return render_template('eventhall_list.html', user=current_user)

@eventhall.route('/eventhall/<id>', methods=["GET"])
def query_salon(id):
    eventhall = Eventhall.query.filter_by(id=id).first()
    if not eventhall:
        return ["Error: Event hall not found"]
    return render_template('eventhall.html', user=current_user, eventhall=eventhall)

@eventhall.route('/register/eventhall', methods=["GET", "POST"])
@login_required
def create_eventhall():
    
    if request.method == 'GET':
        return render_template('register_eventhall.html', user=current_user)
    #POST:
    data = request.form.to_dict(flat=True)
    image = request.files["file"]
    login_user_dto = Eventhall.validate_eventhall(owner_id=current_user.id, **data)
    
    if login_user_dto[0] == False:
        flash(login_user_dto[1], category='error')
        return redirect(url_for('eventhall.create_eventhall'))
    print(login_user_dto)
    if not image:
        flash('Falta cargar imagen', category='error')
        return redirect(url_for('eventhall.create_eventhall'))

    
    eventhall = login_user_dto[0]
    AuthService.create_eventhall(eventhall, image)
    flash('Salón creado exitosamente', category='success')
    return redirect(url_for('eventhall.create_eventhall'))


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




@eventhall.route('/update/eventhall/<eventhallId>', methods=["GET", "POST"])
@login_required
def edit_eventhall(eventhallId):
    eventhall = Eventhall.query.filter_by(id=eventhallId).first()  
    if not eventhall:
        flash(f"Event hall with ID '{eventhallId}' not found", category='error')
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template("put_eventhall.html", user=current_user, eventhall=objToStr(eventhall))
    #POST:
    data = request.form.to_dict(flat=True)

    if "owner_id" in data and eventhall.owner != data.get("owner"):
        flash("No se puede cambiar de dueño", category='error')
        return redirect(url_for('eventhall.edit_eventhall', eventhallId=eventhallId))
    if current_user.id != eventhall.owner_id:
        flash(f"Solo se pueden cambiar tus salones", category='error')
        return redirect(url_for('eventhall.edit_eventhall', eventhallId=eventhallId))
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
        return redirect(url_for('eventhall.edit_eventhall', eventhallId=eventhallId))
    flash('Datos cambiados correctamente', category='success')
    return redirect(url_for('eventhall.edit_eventhall', eventhallId=eventhallId))
