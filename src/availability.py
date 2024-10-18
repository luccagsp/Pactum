from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for
from models import Availability, Eventhall
from auth_service import AuthService
from config.objToStr import objToStr
from config.validateHours import validate_json_hours_structure
from db import db
from upload import query_image
from flask_cors import cross_origin
availability = Blueprint('availability', __name__)


@availability.route('/availability')
def availability_frontend():
    return render_template("availability.html", user=current_user)

@availability.route('/eventhall/<eventhallId>/addAvailability', methods=["POST"])
@login_required
def add_availability(eventhallId):
    print("isJson:", request.is_json)
    data = request.form
    checkedData = validate_json_hours_structure(data)
    if checkedData[0] == False:
        flash(checkedData[1], category='error')
        return redirect(url_for('availability.availability_frontend'))

    availabilityExists = Availability.query.filter_by(eventhall_id=id).first()
    if availabilityExists:
        flash(f"Availability for Event hall with id '{id}' already exists")
        return redirect(url_for('availability.availability_frontend'))
    
    eventhall = Eventhall.query.filter_by(id=id).first()
    if current_user.id != eventhall.owner_id:
        return f"Error: Only event hall owners can change Availability"
    flash(f"Successfully added Availability to Event Hall: '{eventhall.name}'", category='success')
    availability = Availability(eventhall_id=eventhallId, hours=checkedData[1])
    db.session.add(availability)
    db.session.commit()

    return redirect(url_for('availability.availability_frontend'))

@availability.route('/availability/<eventhallId>')
def get_availability(eventhallId):
    availability = Availability.query.filter_by(eventhall_id=eventhallId).first()
    print(availability)
    if not availability: return "None"
    return objToStr(availability)