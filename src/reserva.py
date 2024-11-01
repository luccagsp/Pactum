from datetime import datetime
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for, send_from_directory, current_app
from flask_login import login_required, current_user
from models import User, Eventhall, Image, Reservation
from config.objToStr import objToStr
from db import db
from config.dotenv_handler import Envs

from upload import query_image

reserve = Blueprint('reserve', __name__)

def err(error):
    flash(error, category=error)
def isempty(file):
    if file.filename == '':
        return True
    if file.content_type == 'application/octet-stream': 
        return True
    return False


@reserve.route('/reserve/<int:eventhall_id>', methods=["POST", "GET"])
@login_required
def frontend(eventhall_id):
    # Buscar el salón con el id proporcionado
    eventhall = Eventhall.query.filter_by(id=eventhall_id).first()
    
    if not eventhall:
        flash('Salón no encontrado', category='danger')
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('reservation.html', user=current_user, eventhall=eventhall)
    
    # POST request para procesar la reserva
    date = request.form.get('date')
    time = request.form.get('time')
    file = request.files.get('file')
    image_url=None
    if not isempty(file):
        image_url = query_image(file, eventhall_id, "payment")
        flash('Comprobante subido', category='success')
    user = current_user 

    if eventhall.instant_booking == False and isempty(file) == True:
        flash('Los salones con "reserva instantánea" desactivada requieren de un comprobante de pago', category='danger')
        return redirect(url_for('reserve.frontend', eventhall_id=eventhall_id))
    
    # Crear reserva usando la información proporcionada
    if eventhall.instant_booking == False:
        state="pending"
    else:
        state = "reserved"
    dto = Reservation.from_reserva(
        reservation_time=time, 
        reservation_date=date, 
        eventhall_id=eventhall_id, 
        user_id=user.id, 
        reservation_price=eventhall.reservation_price,
        url_payment=image_url,
        state=state
    )

    # Comprobar si la reserva fue creada correctamente
    if dto[0] == False:
        flash(dto[1], category='danger')
        return redirect(url_for('reserve.frontend', eventhall_id=eventhall_id))

    reservation = dto[1]

    # Guardar la reserva en la base de datos
    db.session.add(reservation)
    db.session.commit()
    flash('Reserva creada exitosamente', category='success')
    return redirect(url_for('index'))
    return redirect(url_for('reserve.frontend', eventhall_id=eventhall_id))



@reserve.route("/reserve/validate/<reserveId>")
def validate(reserveId):
    reserve = Reservation.query.filter_by(id=reserveId).first()
    if not reserve: 
        flash("reserva no encontrada", category="error")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)

    if reserve.deleted_at: 
        flash("reserva ya existente", category="error")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)

    if reserve.validated_at: 
        flash("reserva ya validada", category="error")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)

    eventhall = Eventhall.query.filter_by(id=reserve.eventhall_id).first()
    if not eventhall: 
        flash("salon no encontrado", category="error")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)

    if eventhall.instant_booking == True: 
        flash("salon con reserva instantanea activada", category="error")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)


    setattr(reserve, "validated_at", datetime.now())
    setattr(reserve, "validated_by", current_user.id)
    setattr(reserve, "state", "reserved")
    db.session.commit()
    # setattr(reserve, "validated_by", current_user.id)
    flash("Reserva validada", category="success")
    return redirect(url_for('solicitudes', user=current_user, eventhall_id=eventhall.id))

@reserve.route("/reserve/delete/<reserveId>")
def delete(reserveId):
    reserve = Reservation.query.filter_by(id=reserveId).first()
    if not reserve: 
        flash("reserva no encontrada", category="alert")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)

    eventhall = Eventhall.query.filter_by(id=reserve.eventhall_id).first()
    if not eventhall: 
        flash("salon no encontrado", category="alert")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)

    db.session.delete(reserve)
    db.session.commit()
    flash("Reserva cancelada", category="success")
    return redirect(url_for('solicitudes', user=current_user, eventhall_id=eventhall.id))

@reserve.route("/reserve/cancel/<reserveId>")
def cancel(reserveId):
    reserve = Reservation.query.filter_by(id=reserveId).first()
    if not reserve: 
        flash("reserva no encontrada", category="error")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)

    if reserve.deleted_at: 
        flash("reserva ya existente", category="error")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)

    if reserve.validated_at: 
        flash("reserva ya validada", category="error")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)

    eventhall = Eventhall.query.filter_by(id=reserve.eventhall_id).first()
    if not eventhall: 
        flash("salon no encontrado", category="error")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)

    if eventhall.instant_booking == True: 
        flash("salon con reserva instantanea activada", category="error")
        return url_for('solicitudes', user=current_user, eventhall_id=eventhall.id)


    setattr(reserve, "state", "cancelled")
    db.session.commit()
    flash("Reserva cancelada", category="success")
    return redirect(url_for('solicitudes', user=current_user, eventhall_id=eventhall.id))
