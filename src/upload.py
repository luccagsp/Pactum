import shortuuid
import os
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for, send_from_directory, current_app
from flask_login import login_required, current_user
from models import User, EventHall
from config.objToStr import objToStr
from werkzeug.utils import secure_filename
from db import db

upload = Blueprint('auth', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

#Verifica si la extensión del archivo es valida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload.route('/upload/<eventhallId>', methods=["POST"])
@login_required
def upload(eventhallId):
    eventhall = EventHall.query.filter_by(eventhallId).first()
    if eventhall.owner_id != current_user.id:
        return "Solo los dueños dell salón pueden agregar imágenes"
    file = request.files["file"]
    filename = secure_filename(file.filename)
    if not file:
        return "Falta 'file'"
    if not allowed_file(filename):
        return f"Extensión de 'file' invalida. Extensiones validas: {ALLOWED_EXTENSIONS}"
    
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)) # Then save the file


    name = "text.txt"
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], shortuuid.uuid())

@upload.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

upload.run(debug=True)

