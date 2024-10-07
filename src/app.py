from pathlib import Path
from config.objToStr import objToStr
from flask import Flask, render_template, request
from flask_login import LoginManager, login_required, current_user
from config.dotenv_handler import Envs
from db import create_db
#Inicializaciones
app = Flask(__name__)
envs = Envs()
# Configurando parametros de app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = envs.SECRET
# Inicializando BBDD y despúes importando sus modelos y servicios
db = create_db(app)
from models.user import User
from models.eventhall import EventHall
from models.availability import Availability
from models.reservation import Reservation
#Sistema de login, se inicizliza despues de inicializar la BBDD
login_manager = LoginManager()
## login_manager.login_view = 'auth.login' <-- qué función está encargada del login view
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    user = User.query.filter_by(id=id).first()
    # print(user)
    return user
#Blueprints
from auth_blueprint import auth_blueprint
app.register_blueprint(auth_blueprint)


@app.route('/')
def home():
    return render_template("index.html")
@app.route('/reserve')
@login_required
def reserve():
    data = request.get_json()
@app.route('/eventhall/<id>', methods=["PUT"])
@login_required
def edit_eventhall(id):
    data = request.get_json()
    eventhall:EventHall = db.session.get(EventHall, 1)
    print(eventhall)
    
    if not eventhall:
        return["eventhall not found"]
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

    # for i in data:
    #     print(**data)

    return objToStr(eventhall)

@app.route('/eventhall/<id>', methods=["GET"])
def query_salon(id):

    nombre_salon = request.args.get('nombre_salon')
    print(nombre_salon)
    data:EventHall = EventHall.query.filter_by(name=nombre_salon).first() 
    
    if data:
        return {'id' : data.id, 'nombre' : data.nombre, 'descripcion' : data.descripcion, 'calle_domicilio' : data.calle_domicilio, 'numero_domicilio' : data.numero_domicilio, 'email_contacto' : data.email_contacto, 'telefono_contacto' : data.telefono_contacto, 'precio_sena' : data.precio_sena, 'imagenes' : data.imagenes, 'reserva_instantanea' : data.reserva_instantanea, 'creado_en' : data.creado_en, 'actualizado_en' : data.actualizado_en} 
    else:
        return ["Error: Event hall not found"]

if __name__ == "__main__":
    if not Path('../instance/project.db'):
        #Crear BBDD
        with app.app_context():
            db.create_all()

        from os import path
        print(f"Database successfully created in '{path.abspath('../instance/project.db')}'")
        print(f"Please reload app")
    else:
        app.run(debug=True ,port=5000)
