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
    # salon = EventHall()
    # db.session.add(salon)
    # db.session.commit()

    return render_template("index.html")
@app.route('/auth/register/user', methods=["GET", "POST"])
def register_user():
    #Tomando JSON
    data = request.get_json()
    try:
        nombre = data['nombre']
        apellido = data['apellido']
        email = data['email']
        phone = data['telefono']
        password = data['password']
    except KeyError as err:
        print(f"Error: falta la clave '{err.args[0]}' en el JSON recibido.")
        return {"error": f"Falta la clave '{err.args[0]}' en el JSON."}, 400
    validate_user_dto = validate_data(nombre, apellido, email, phone, password)
    if validate_user_dto[0] != None:
        return validate_user_dto
    user = validate_user_dto[1]
    response = auth_service.create_user(user)
    return response
    # return render_template("index.html")
@app.route('/auth/register/eventhall', methods=["GET", "POST"])
def register_eventhall():
    #Tomando JSON
    data = request.get_json()
    try:    
        # name = data['owner']
        name = data['name']
        deposit_price = data['deposit_price']
        instant_booking = data['instant_booking']
    except KeyError.args[0] == 'deposit_price':
        return ["el deposito crack"]
    except KeyError as err:
        print(f"Error: falta la clave '{err.args[0]}' en el JSON recibido.")
        return {"error": f"Falta la clave '{err.args[0]}' en el JSON."}, 400
    
    # validate_user_dto = validate_data(name=name, email=email, phone=phone, deposit_price=deposit_price)

    # if validate_user_dto[0] != None:
    #     return validate_user_dto

    # auth_service.create_eventhall(db)
    # usuario = EventHall(name=name, email=email, phone=phone, deposit_price=deposit_price)
    # db.session.add(usuario)
    # db.session.commit()
    return render_template("index.html")


@app.route('/salon')
def query_salon():

    nombre_salon = request.args.get('nombre_salon')
    print(nombre_salon)
    data:EventHall = EventHall.query.filter_by(name=nombre_salon).first() 
    
    if data:
        dict_data = {'id' : data.id, 'nombre' : data.nombre, 'descripcion' : data.descripcion, 'calle_domicilio' : data.calle_domicilio, 'numero_domicilio' : data.numero_domicilio, 'email_contacto' : data.email_contacto, 'telefono_contacto' : data.telefono_contacto, 'precio_sena' : data.precio_sena, 'imagenes' : data.imagenes, 'reserva_instantanea' : data.reserva_instantanea, 'creado_en' : data.creado_en, 'actualizado_en' : data.actualizado_en}
    else: dict_data = {} # Si la variable 'data' no encuentra ningun usuario...

    return dict_data

if __name__ == "__main__":
    # app.add_url_rule('/query_string',view_func=query_string)
    app.run(debug=True ,port=5000)

    #Crear BBDD
    # with app.app_context():
    #         db.create_all()