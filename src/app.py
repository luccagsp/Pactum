import os
from pathlib import Path
from flask import Flask, render_template, request, flash
from flask_login import LoginManager, login_required, current_user
from config.objToStr import objToStr
from config.dotenv_handler import Envs
from db import create_db
from werkzeug.exceptions import RequestEntityTooLarge
from flask_cors import CORS

# Obtener el directorio del archivo que se está ejecutando
current_directory = os.path.dirname(os.path.abspath(__file__))
# Ir una carpeta atrás
parent_directory = os.path.dirname(current_directory)
#Seleccionar carpeta images
folder_path = os.path.join(parent_directory, 'images')

if not os.path.exists(folder_path):
        os.makedirs(folder_path)

#InicializacionesF
app = Flask(__name__)
CORS(app, supports_credentials=True)
envs = Envs()
# Configurando parametros de app
app.config["UPLOAD_FOLDER"] = folder_path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = envs.SECRET
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB de limite
@app.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    flash('Archivo demasiado grande. Tamaño máximo: 5MB', category='danger')
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
from reserva import reserve
from availability import availability
app.register_blueprint(auth)
app.register_blueprint(upload)  
app.register_blueprint(eventhall)
app.register_blueprint(reserve)
app.register_blueprint(availability)


@app.route('/', methods=["GET"])
def index():
    eventhalls = Eventhall.query.limit(10).all()
    return render_template('home.html', user=current_user, eventhalls=eventhalls)

@app.route('/register_eventhall', methods=["GET", "POST"])
def register_eventhall():
    return render_template("register_eventhall.html", user=current_user)

@app.route('/reservation/<id>', methods=["GET", "POST"])
def reservation(id):
    eventhall = Eventhall.query.filter_by(id=id).first()
    if not eventhall:
        return ["Error: Event hall not found"]
    return render_template("reservation.html", user=current_user, eventhall=eventhall)

def main():
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
            db.session.add(User(name="admin", surname="admin", phone='543564609683', email="admin@gmail.com", password=BcryptAdapter.hash(password='admin')))
            db.session.add(Eventhall(alias="puerto.aventura", name="Puerto aventura", reservation_price=3000, owner_id=1, street_number="123", street_address="Juan de Garay"))
            db.session.add(Eventhall(alias="asd.aventura", name="Kopate", reservation_price=1232, owner_id=1, instant_booking=False, street_number="1200", street_address="Alfredo Goiran"))
            db.session.commit()
            print("Successfully created default user for Users and eventhall for Eventhalls")
        app.run(debug=True ,port=5000)
    else:
        app.run(debug=True ,port=5000)


if __name__ == "__main__":
    main()