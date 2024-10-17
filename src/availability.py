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
def get_availability():
    print("aloja")
    return render_template("availability.html", user=current_user)

@availability.route('/eventhall/<id>/addAvailability', methods=["POST"])
@login_required
def add_availability(id):
    print("json", request.is_json)
    data = request.form
    checkedData = validate_json_hours_structure(data)
    if checkedData[0] == False:
        flash(checkedData[1], category='error')
        print("blakc")
        return redirect(url_for('eventhall.availability'))
    eventhallId = request.form.get('eventhallId')
    print(eventhallId) 
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