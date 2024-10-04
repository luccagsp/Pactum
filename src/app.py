from pathlib import Path
from flask import Flask, render_template, request
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
from models.user import User, validate_data
from models.eventhall import EventHall
from models.availability import Availability
from models.reservation import Reservation
import auth_service as auth_service

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/auth/register/user', methods=["GET", "POST"])
def register_user():
    #Tomando JSON
    data = request.get_json()
    validate_user_dto = validate_data(**data)

    if validate_user_dto[0] != None:
        return validate_user_dto
    
    user = validate_user_dto[1]
    response = auth_service.create_user(user)
    return response
    # return render_template("index.html")

@app.route('/auth/register/eventhall', methods=["GET", "POST"])
def register_eventhall():
    data = request.get_json()
    print(data)

    validate_hall_dto = EventHall.validate_eventhall(**data)
    print(validate_hall_dto)
    if validate_hall_dto[0] != None:
        return validate_hall_dto

    # auth_service.create_eventhall(db)

    return render_template("index.html")

@app.route('/salon/<id>', methods=["GET"])
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
