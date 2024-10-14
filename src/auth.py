from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for
from models import User, Eventhall
from auth_service import AuthService
from config.objToStr import objToStr
auth = Blueprint('auth', __name__)

@auth.route('/register/user', methods=["GET", "POST"])
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
@auth.route('/login', methods=["GET", "POST"])
def login_user():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        login_user_dto = User.login_user_dto(**data)

        res = AuthService.log_in_user(login_user_dto)
        if res[0] == False:
            flash(res[1], category='error')
            return redirect(url_for('auth.login_user')) #Usando POST-Redirect-GET pattern

        flash("Successfully logged", category='success')
        # return ["Successfully logged"]
    if not current_user.is_authenticated:
        return render_template('login.html', user=current_user)
    return redirect("http://localhost:5000/")


@auth.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', category='success')
    return redirect("http://localhost:5000/", code=302)

@auth.route('/current')
def current():
    return jsonify(objToStr(current_user))
