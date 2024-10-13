import os
from pathlib import Path
from flask import Flask, render_template, request, flash
from flask_login import LoginManager, login_required, current_user
from config.objToStr import objToStr
from config.dotenv_handler import Envs
from db import create_db
from werkzeug.exceptions import RequestEntityTooLarge


# Obtener el directorio del archivo que se está ejecutando
current_directory = os.path.dirname(os.path.abspath(__file__))
# Ir una carpeta atrás
parent_directory = os.path.dirname(current_directory)
#Seleccionar carpeta images
folder_path = os.path.join(parent_directory, 'images')
#Inicializaciones
app = Flask(__name__)
envs = Envs()
# Configurando parametros de app
app.config["UPLOAD_FOLDER"] = folder_path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = envs.SECRET
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB de limite
@app.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    flash('Archivo demasiado grande. Tamaño máximo: 5MB', category='error')
    return 'Archivo demasiado grande. Tamaño máximo: 5MB', 413

# Inicializando BBDD y despúes importando sus modelos y servicios
db = create_db(app)
from models import Availability, Eventhall, Reservation, User, Image
#Sistema de login, se inicizliza despues de inicializar la BBDD
login_manager = LoginManager()
## login_manager.login_view = 'auth.login' <-- qué función está encargada del login view
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    user = User.query.filter_by(id=id).first()
    return user
#Blueprints
from auth import auth
from upload import upload
from eventhall import eventhall
app.register_blueprint(auth)
app.register_blueprint(upload)
app.register_blueprint(eventhall)


@app.route('/')
def home():
    return render_template("base.html", user=current_user)
@app.route('/availability')
def availability():
    return render_template("availability.html", user=current_user)

if __name__ == "__main__":
    from pathlib import Path
    from os import path
    from config.bcrypt_adapter import BcryptAdapter
    BcryptAdapter = BcryptAdapter()
    database = Path("././instance/project.db")
    if not database.is_file():
        #Crear BBDD
        with app.app_context():
            db.create_all()
            print(f"Database successfully created in '{path.abspath('../instance/project.db')}'")
            db.session.add(User(name="Lucca", surname="Martina", phone='543564609685', email="lccmartina@gmail.com", password=BcryptAdapter.hash(password='luccamartina')))
            db.session.add(Eventhall(name="Puerto aventura", deposit_price=3000, owner_id=1))
            db.session.commit()
            print("Successfully created default user for Users and eventhall for Eventhalls")
        app.run(debug=True ,port=5000)

    else:
        app.run(debug=True ,port=5000)
