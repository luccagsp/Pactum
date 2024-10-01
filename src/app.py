from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import JSON
from envconfig import Envs
from models.user import validate_data as validate_user
envs = Envs()
class Base(DeclarativeBase):
  pass

# create the app
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = envs.SECRET
# initialize the app with the extension before the config
db.init_app(app)

class Salon(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(20), nullable=False)
  descripcion = db.Column(db.String(2200))
  calle_domicilio = db.Column(db.String(80))
  numero_domicilio = db.Column(db.String(2200))
  email_contacto = db.Column(db.String(255), nullable=False)
  telefono_contacto = db.Column(db.String(20), nullable=False)
  precio_sena = db.Column(db.Integer, nullable=False)
  imagenes = db.Column(JSON)
  reserva_instantanea = db.Column(db.Boolean, default=True)
  creado_en = db.Column(db.DateTime, default=func.now())  # Columna timestamp con valor por defecto de la hora actual
  actualizado_en = db.Column(db.DateTime, default=func.now())  # Columna timestamp con valor por defecto de la hora actual
  db.relationship('Address', backref='person', lazy=True)

class Reserva(db.Model, UserMixin):    
    id = db.Column(db.Integer, primary_key=True)
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha_reserva = db.Column(db.DateTime, nullable=False)
    hora_reserva = db.Column(db.DateTime, nullable=False)
    url_comprobante_pago = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(50), default="Pendiente")
    validado_por = db.Column(db.Integer)
    validado_en = db.Column(db.DateTime)
    creado_en = db.Column(db.DateTime, default=func.now())
    actualizado_en = db.Column(db.DateTime, default=func.now())

class Disponibilidad(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'), nullable=False)
    horarios = db.Column(db.JSON, nullable=False)
    creado_en = db.Column(db.DateTime, default=func.now())
    actualizado_en = db.Column(db.DateTime, default=func.now())

class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    apellido = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    profile_pic = db.Column(db.TEXT)

    # Relación con Reserva
    reservas = db.relationship('Reserva', backref='cliente', lazy='dynamic')


@app.route('/')
def home():
    salon = Salon(nombre="pene aventura", email_contacto='penerete@gmail.com', telefono_contacto='+54545454', precio_sena=777)
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

    validate_user_dto = validate_user(nombre, apellido, email, phone)
    
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