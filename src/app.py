from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import JSON
from envconfig import Envs
envs = Envs()
print(envs.SECRET)
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
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    profile_pic = db.Column(db.TEXT, nullable=False)

    # Relación con Reserva
    reservas = db.relationship('Reserva', backref='cliente', lazy='dynamic')

# with app.app_context():
#     db.create_all()
@app.route('/')
def home():
    usuario = Cliente(nombre="cliente", email="asdasasssdd", phone="asdsdssdasd", profile_pic="sdasdassa")
    db.session.add(usuario)
    db.session.commit()
    print("hecho!")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)