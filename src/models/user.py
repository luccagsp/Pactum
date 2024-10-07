import config.regular_exps as regular_exps
from db import db, UserMixin
from config.phonenumbers_handler import verify_phone
class LoginUserDto:
    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    profile_pic = db.Column(db.TEXT)
    password = db.Column(db.String(72), nullable = False)

    # Relación con Reserva
    # reservas = db.relationship('Reserva', backref='cliente', lazy='dynamic')

    def from_user(nombre:str, apellido:str, email:str, phone:str, password:str) -> list:
        if type(nombre) != str or type(apellido) != str or type(email) != str or type(password) != str:
            return ["Name, surname, email and password must be strings"]
        if len(nombre) > 20 or len(apellido) > 40 or " " in nombre or " " in apellido:
            return ["Name or surname not valid"]
        if regular_exps.email.match(email) == None:
            return ["Invalid email"]
        if verify_phone(phone) == False:
            return ["Invalid phone"]

        return[None, User(name=nombre, surname=apellido, email=email, phone=phone, password=password)]
        # return[None, {'nombre':nombre, 'apellido':apellido, 'email':email, 'phone':phone}]
    def login_user_dto(email, password):
        return LoginUserDto(email,password)