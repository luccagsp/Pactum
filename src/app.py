from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from sqlalchemy import JSON
from envconfig import Envs

from db import create_db
envs = Envs()

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = envs.SECRET
# initialize the app with the extension before the config
db = create_db(app)
from models.user import Cliente, validate_data
from models.availability import Disponibilidad
from models.reservation import Reserva
from models.eventhall import Salon


@app.route('/')
def home():
    salon = Salon(nombre="puerto aventura", email_contacto='gmail@gmail.com', telefono_contacto='+54545454', precio_sena=777)
    db.session.add(salon)
    db.session.commit()
    # print(request.get_json())
    # usuario = Cliente(nombre="cliente", email="asdasasssdd", phone="asdsdssdasd", profile_pic="sdasdassa")
    # db.session.add(usuario)
    # db.session.commit()
    print("hecho!")
    return render_template("index.html")
@app.route('/auth/register/user', methods=["GET", "POST"])
def register_user():
    #Tomando JSON
    data = request.get_json()
    nombre = data['nombre']
    apellido = data['apellido']
    email = data['email']
    phone = data['telefono']

    validate_user_dto = validate_data(nombre, apellido, email, phone)
    
    #Si retorna error el DTO
    if validate_user_dto[0] != None:
        return validate_user_dto


    usuario = Cliente(nombre=nombre, email=email, phone=phone, apellido=apellido)
    db.session.add(usuario)
    db.session.commit()
    return render_template("index.html")


@app.route('/salon')
def query_salon():
    nombre_salon = request.args.get('nombre_salon')
    print(nombre_salon)
    data:Salon = Salon.query.filter_by(nombre= nombre_salon).first() 
    dict_data = {}
    if data:
        dict_data = {'id' : data.id, 'nombre' : data.nombre, 'descripcion' : data.descripcion, 'calle_domicilio' : data.calle_domicilio, 'numero_domicilio' : data.numero_domicilio, 'email_contacto' : data.email_contacto, 'telefono_contacto' : data.telefono_contacto, 'precio_sena' : data.precio_sena, 'imagenes' : data.imagenes, 'reserva_instantanea' : data.reserva_instantanea, 'creado_en' : data.creado_en, 'actualizado_en' : data.actualizado_en}
    return dict_data

if __name__ == "__main__":
    # app.add_url_rule('/query_string',view_func=query_string)
    app.run(debug=True, port=5000)

    #Crear BBDD
    # with app.app_context():
    #         db.create_all()