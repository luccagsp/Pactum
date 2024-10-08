from pathlib import Path
from flask import Flask, render_template, request, flash
from flask_login import LoginManager, login_required, current_user
from config.objToStr import objToStr
from config.dotenv_handler import Envs
from db import create_db
#Inicializaciones
app = Flask(__name__)
envs = Envs()
# Configurando parametros de app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = envs.SECRET
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}

# Inicializando BBDD y despúes importando sus modelos y servicios
db = create_db(app)
from models import EventHall, Reservation, User
from auth_service import AuthService
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
app.register_blueprint(auth)


@app.route('/')
def home():
    return render_template("base.html", user=current_user)
@app.route('/eventhall/<id>', methods=["PUT"])
@login_required
def edit_eventhall(id):
    data = request.get_json()
    eventhall:EventHall = EventHall.query.filter_by(id=id).first()  
    
    if not eventhall:
        return[f"Event hall with ID '{id}' not found"]
    if "owner" in data and eventhall.owner != data.get("owner"):
        return["No se puede cambiar de dueño, flaco, picá de acá"]
    if current_user.id != eventhall.owner:
        return ["Este no es tu salón, flaco, picá de acá"]
    
    for column in data:
        setattr(eventhall, column, data[column]) # Actualiza eventhall
    destructured_eventhall = objToStr(eventhall)
    destructured_eventhall.pop('id', None)
    destructured_eventhall.pop('updated_at', None)
    destructured_eventhall.pop('created_at', None)

    if EventHall.validate_eventhall(**destructured_eventhall)[0] == None:
        db.session.commit()

    return objToStr(eventhall)

@app.route('/')
@app.route('/eventhall/<id>', methods=["GET"])
def query_salon(id):

    nombre_salon = request.args.get('nombre_salon')
    print(nombre_salon)
    data:EventHall = EventHall.query.filter_by(name=nombre_salon).first() 
    
    if not data:
        return ["Error: Event hall not found"]
    return {'id' : data.id, 'nombre' : data.nombre, 'descripcion' : data.descripcion, 'calle_domicilio' : data.calle_domicilio, 'numero_domicilio' : data.numero_domicilio, 'email_contacto' : data.email_contacto, 'telefono_contacto' : data.telefono_contacto, 'precio_sena' : data.precio_sena, 'imagenes' : data.imagenes, 'reserva_instantanea' : data.reserva_instantanea, 'creado_en' : data.creado_en, 'actualizado_en' : data.actualizado_en} 

@app.route('/eventhall/<id>/addAvailability', methods=["POST"])
@login_required
def add_availability(id):
    data = request.get_json()
    
    availabilityExists = Availability.query.filter_by(eventhall_id=id).first()
    if availabilityExists:
        return [f"Error: Availability for Event hall with id '{id}' already exists"]
    if data[0] == False: #Si el verificador retorna 'False'
        return [f"Error: Invalid hours structure: {data[1]}"]
    
    eventhall = EventHall.query.filter_by(id=id).first()
    if current_user.id != eventhall.owner_id:
        return f"Error: Only event hall owners can change Availability"
    flash(f"Successfully added Availability to Event Hall: '{eventhall.name}'", category='success')
    availability:Availability = Availability(eventhall_id=id, hours=data)
    db.session.add(availability)
    db.session.commit()

    print(objToStr(availability))
    return objToStr(availability)


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
            db.session.add(EventHall(name="Puerto aventura", deposit_price=3000, owner_id=1))
            db.session.commit()
            print("Successfully created default user for Users and eventhall for EventHalls")
        app.run(debug=True ,port=5000)

    else:
        app.run(debug=True ,port=5000)
