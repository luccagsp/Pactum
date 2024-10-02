import config.regular_exps as regular_exps


from db import db, UserMixin
from config.phonenumbers_handler import verify_phone

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    profile_pic = db.Column(db.TEXT)
    password = db.Column(db.String(255), nullable = False)

    # Relación con Reserva
    reservas = db.relationship('Reserva', backref='cliente', lazy='dynamic')

def validate_data(nombre, apellido, email, phone) -> list:
    if len(nombre) > 20 or len(apellido) > 20 or " " in nombre or " " in apellido:
        return ["Nombre o apellido invalidos"]
    if regular_exps.email.match(email) == None:
        return ["Email invalido"]
    if verify_phone(phone) == False:
        return ["Numero de telefono invalido"]

    return[None, User(name=nombre, surname=apellido, email=email, phone=phone)]
    # return[None, {'nombre':nombre, 'apellido':apellido, 'email':email, 'phone':phone}]