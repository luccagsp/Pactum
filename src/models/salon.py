from db import db, UserMixin
from sqlalchemy import JSON
from sqlalchemy.sql import func

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
