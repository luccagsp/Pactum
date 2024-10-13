import shortuuid
import os
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for, send_from_directory, current_app
from flask_login import login_required, current_user
from models import User, Eventhall, Image
from config.objToStr import objToStr
from werkzeug.utils import secure_filename
from db import db
from config.dotenv_handler import Envs
upload = Blueprint('upload', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

#Verifica si la extensión del archivo es valida
def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return filename.rsplit('.', 1)[1].lower()
    return None

@upload.route('/upload', methods=["POST", 'GET'])
@login_required
def upload_image():
    if request.method == "GET":
        return render_template('upload.html', user=current_user)
    #POST:
    eventhallId = request.form["eventhallId"]
    eventhall = Eventhall.query.filter_by(id=eventhallId).first()
    if not eventhall:
        return "Salón de eventos no encontrado",404
    if eventhall.owner_id != current_user.id:
        return "Solo los dueños del salón pueden agregar imágenes"
    file = request.files["file"]
    if not file:
        return "Falta 'file'"
    filename = secure_filename(file.filename)
    if not allowed_file(filename):
        return f"Extensión de 'file' invalida. Extensiones validas: {ALLOWED_EXTENSIONS}"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    fileExtension = f".{filename.rsplit('.', 1)[1].lower()}"
    filename = f"{shortuuid.uuid()}{fileExtension}" #Cambia el nombre del archivo a un UUID
    file.save(os.path.join(upload_folder, filename)) # Then save the file

    image_url = f"{Envs.ROOT_URL}{url_for('upload.uploaded_file', filename=filename)}"
    image:Image = Image(eventhall_id=eventhallId, file_url=image_url)
    db.session.add(image)
    db.session.commit()
    
    return image_url

@upload.route('/upload/<filename>', methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


