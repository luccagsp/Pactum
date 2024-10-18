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


@reserve.route('/reserve/<eventhallId>', methods=["POST", "GET"])
@login_required
def frontend(eventhallId):
    if request.method == 'GET':
        return render_template('reservar.html', user=current_user)
    #POST:
    date=request.form.get('date')
    time=request.form.get('time')
    user = current_user 
    eventhall = Eventhall.query.filter_by(id=eventhallId).first()

    if not eventhall:
        flash('Salón no encontrado', category='error')
        return redirect(url_for('reserve.frontend', eventhallId=eventhallId))
    
    dto = Reservation.from_reserva(reservation_time=time, reservation_date=date, eventhall_id=eventhallId, user_id=user.id, reservation_price=eventhall.reservation_price)
    if dto[0] == False:
        flash(dto[1], category='error')
        return redirect(url_for('reserve.frontend', eventhallId=eventhallId))

    reservation = dto[1]
    if eventhall.instant_booking == False and reservation.url_payment == None:
        flash('Los salones con reserva instantanea desactivada requieren de un comprobante de pago', category='error')
        return redirect(url_for('reserve.frontend', eventhallId=eventhallId))
    print(objToStr(reservation))
    db.session.add(reservation)
    db.session.commit()
    flash('Reserva creada exitosamente', category='success')
    return redirect(url_for('reserve.frontend', eventhallId=eventhallId))

