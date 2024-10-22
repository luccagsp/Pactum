import shortuuid
import os
import base64
from datetime import datetime
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

def query_image(file, eventhallId, type_image='image'):
    filename = secure_filename(file.filename)
    if not allowed_file(filename):
        flash(f"Extensión de 'file' invalida. Extensiones validas: {ALLOWED_EXTENSIONS}")
        return f"Extensión de 'file' invalida. Extensiones validas: {ALLOWED_EXTENSIONS}"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    fileExtension = f".{filename.rsplit('.', 1)[1].lower()}"
    filename = f"{shortuuid.uuid()}{fileExtension}" #Cambia el nombre del archivo a un UUID
    
    # Convertir a Base64
    file_data = base64.b64encode(file.read()).decode('utf-8')

   # file.save(os.path.join(upload_folder, filename)) # Then save the file


    image_url = f"{Envs.ROOT_URL}{url_for('upload.uploaded_file', filename=filename)}"
    image:Image = Image(eventhall_id=eventhallId, file_url=image_url, type_image=type_image, filename=filename, file_data=file_data)
    db.session.add(image)
    db.session.commit()

    return image_url

@upload.route('/upload/<eventhallId>', methods=["POST", 'GET'])
@login_required
def upload_image(eventhallId):
    eventhall = Eventhall.query.filter_by(id=eventhallId).first()
    if not eventhall:
        flash('salón de eventos no encontrado', category='error')
        return redirect(url_for('index'))
    if current_user.eventhalls == []:
        flash('Para subir imagenes necesitas salones asociados a tu usuario', category='error')
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template('upload.html', user=current_user, eventhall=eventhall)
    
    #POST:
    # eventhallId = request.form["eventhallId"]
    
    if eventhall.owner_id != current_user.id:
        return "Solo los dueños del salón pueden agregar imágenes"
    file = request.files["file"]
    if not file:
        return "Falta 'file'"
    image_url = query_image(file, eventhallId)
    
    return image_url

@upload.route('/upload/view/<filename>', methods=["GET"])

def uploaded_file(filename):
    image = Image.query.filter_by(filename=filename).first()
    if not image:
        return "imagen no encontrada", 404
    if image.deleted_at != None:
        return "imagen no encontrada", 404
    return jsonify({'image': image.file_data})
    #return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@upload.route('/upload/delete/<imageId>')
def delete(imageId):
    print(current_app.config['UPLOAD_FOLDER'])
    image = Image.query.filter_by(id=imageId).first()
    if not image:
        flash(f'Imagen con id:"{imageId}", no encontrada', category='error')
        return redirect(url_for('index'))
    if image.deleted_at != None:
        flash(f'Imagen con id:"{imageId}", actualmente eliminada', category='error')
        return redirect(url_for('index'))
    eventhall_ids = [eventhall.id for eventhall in current_user.eventhalls]
    if image.eventhall_id not in eventhall_ids:
        print(eventhall_ids)
        flash(f'Solo los dueños de salones pueden borrar imagenes', category='error')
        return redirect(url_for('index'))
    upload_folder = current_app.config['UPLOAD_FOLDER']

    db.session.delete(image)
    db.session.commit()
    os.remove(os.path.join(upload_folder, image.filename))

    flash(f'Imagen eliminada exitosamente', category='success')
    return redirect(url_for('index'))
