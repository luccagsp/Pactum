from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, render_template, jsonify
from models import User, EventHall
from auth_service import AuthService
from config.objToStr import objToStr
auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/auth/register/user', methods=["GET", "POST"])
def register_user():
    #Tomando JSON
    data = request.get_json()
    validate_user_dto = User.from_user(**data)

    if validate_user_dto[0] != None:
        return validate_user_dto
    
    user = validate_user_dto[1]
    response = AuthService.create_user(user)
    return response
    # return render_template("index.html")
@auth_blueprint.route('/auth/login/user', methods=["GET", "POST"])
def login_user():
    data = request.get_json()
    login_user_dto = User.login_user_dto(**data)

    AuthService.log_in_user(login_user_dto)
    return "Successfully loged"


@auth_blueprint.route('/auth/register/eventhall', methods=["GET", "POST"])
@login_required
def register_eventhall():
    data = request.get_json()
    userId = current_user.id
    validate_hall_dto = EventHall.validate_eventhall(**data, owner=userId)
    if validate_hall_dto[0] != None:
        return validate_hall_dto
    eventhall = validate_hall_dto[1]
    print(userId, eventhall)
    AuthService.create_eventhall(eventhall)

    return render_template("index.html")


@auth_blueprint.route('/auth/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return render_template('index.html')
@auth_blueprint.route('/current')
def current():
    return jsonify(objToStr(current_user))
