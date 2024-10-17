import shortuuid
import os
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for, send_from_directory, current_app
from flask_login import login_required, current_user
from models import User, Eventhall, Image, Reservation
from config.objToStr import objToStr
from werkzeug.utils import secure_filename
from db import db
from config.dotenv_handler import Envs
reserve = Blueprint('reserve', __name__)

@reserve.route('/reservar/<eventhallId>')
@login_required
def create_reserve(eventhallId):
    user = current_user
    if request.method == 'GET':
        return render_template('reservar.html', user=current_user)
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
    flash('Salón creado exitosamente', category='success')
    return redirect(url_for('eventhall.create_eventhall'))
