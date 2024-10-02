import config.regular_exps as regular_exps
from config.phonenumbers_handler import verify_phone
from db import db, UserMixin
from sqlalchemy import JSON
from sqlalchemy.sql import func

class EventHall(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  description = db.Column(db.String(2200))
  street_address = db.Column(db.String(80))
  place_number = db.Column(db.String(2200))
  email = db.Column(db.String(255), nullable=False)
  phone = db.Column(db.String(20), nullable=False)
  deposit_price = db.Column(db.Integer, nullable=False)
  images = db.Column(JSON)
  instant_booking  = db.Column(db.Boolean, default=True)
  created_at = db.Column(db.DateTime, default=func.now())  # Columna timestamp con valor por defecto de la hora actual
  updated_at = db.Column(db.DateTime, default=func.now())  # Columna timestamp con valor por defecto de la hora actual
  db.relationship('Address', backref='person', lazy=True)

def validate_eventhall(owner, name, email, phone, deposit_price, instant_booking = False):

  # Verifica que no haya espacios al principio ni al final
  if name != name.strip():
      return ["Error: nombre invalido"]
  # Expresión regular para verificar solo caracteres alfanuméricos y espacios
  if not regular_exps.name.match(name):
      return ["Error: nombre invalido"]
  if not regular_exps.email.match(email):
      return ["Error: email invalido"]
  if verify_phone(phone) == False:
      return ["Error: numero de telefono invalido"]


  return [None, EventHall(owner, name, email, phone, deposit_price, instant_booking)]
print("ACA ABAJO")
print("In module products __package__, __name__ ==", __package__, __name__)
print(__name__)