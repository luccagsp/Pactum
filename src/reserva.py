from datetime import datetime
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for, send_from_directory, current_app
from flask_login import login_required, current_user
from models import User, Eventhall, Image, Reservation
from config.objToStr import objToStr
from db import db
from config.dotenv_handler import Envs
reserve = Blueprint('reserve', __name__)

def err(error):
    flash(error, category=error)


@reserve.route('/reserve/<int:eventhall_id>', methods=["POST", "GET"])
@login_required
def frontend(eventhall_id):
    # Buscar el salón con el id proporcionado
    eventhall = Eventhall.query.filter_by(id=eventhall_id).first()
    
    if not eventhall:
        flash('Salón no encontrado', category='error')
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('reservation.html', user=current_user, eventhall=eventhall)
    
    # POST request para procesar la reserva
    date = request.form.get('date')
    time = request.form.get('time')
    file = request.files.get('file')
    print(file)
    user = current_user 
    
    if eventhall.instant_booking == False:
        flash('Los salones con "reserva instantánea" desactivada requieren de un comprobante de pago', category='error')
        return redirect(url_for('reserve.frontend', eventhall_id=eventhall_id))
    # Crear reserva usando la información proporcionada
    dto = Reservation.from_reserva(
        reservation_time=time, 
        reservation_date=date, 
        eventhall_id=eventhall_id, 
        user_id=user.id, 
        reservation_price=eventhall.reservation_price
    )

    # Comprobar si la reserva fue creada correctamente
    if dto[0] == False:
        flash(dto[1], category='error')
        return redirect(url_for('reserve.frontend', eventhall_id=eventhall_id))

    reservation = dto[1]

    # Validar si se necesita comprobante de pago
    if eventhall.instant_booking == False and reservation.url_payment == None:
        flash('Los salones con reserva instantánea desactivada requieren de un comprobante de pago', category='error')
        return redirect(url_for('reserve.frontend', eventhall_id=eventhall_id))

    # Guardar la reserva en la base de datos
    db.session.add(reservation)
    db.session.commit()
    flash('Reserva creada exitosamente', category='success')
    return redirect(url_for('index'))
    return redirect(url_for('reserve.frontend', eventhall_id=eventhall_id))


@reserve.route("/reserve/<reserveId>", methods=["DELETE"])
@login_required
def delete(reserveId):
    reserve = Reservation.query.filter_by(id=reserveId).first()
    setattr(reserve, "deleted_at", datetime.now())
    print(objToStr(reserve))
    db.session.commit()
    flash('reserva eliminada exitosamente', category='success')
    return redirect(url_for('upload.frontend'))

@reserve.route("/reserve/validate/<reserveId>")
def validate(reserveId):
    reserve = Reservation.query.filter_by(id=reserveId).first()
    if not reserve: 
        flash("reserva no encontrada", category="error")
        return "reserva no encontrada"
    if reserve.deleted_at: 
        flash("reserva ya existente", category="error")
        return "reserva ya existente"
    if reserve.validated_at: 
        flash("reserva ya validada", category="error")
        return "reserva ya validada"
    eventhall = Eventhall.query.filter_by(id=reserve.eventhall_id).first()
    if not eventhall: 
        flash("salon no encontrado", category="error")
        return "salon no encontrado"
    if eventhall.instant_booking == True: 
        flash("salon con reserva instantanea activada", category="error")
        return "salon con reserva instantanea activada"

    setattr(reserve, "validated_at", datetime.now())
    db.session.commit()
    # setattr(reserve, "validated_by", current_user.id)
    return "success"