from db import db, UserMixin
from sqlalchemy import JSON
from sqlalchemy.sql import func

class EventHall(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  name = db.Column(db.String(20), nullable=False)
  description = db.Column(db.String(2200))
  street_address = db.Column(db.String(80))
  placee_number = db.Column(db.String(2200))
  email = db.Column(db.String(255), nullable=False)
  phone = db.Column(db.String(20), nullable=False)
  deposit_price = db.Column(db.Integer, nullable=False)
  images = db.Column(JSON)
  instant_booking  = db.Column(db.Boolean, default=True)
  created_at = db.Column(db.DateTime, default=func.now())  # Columna timestamp con valor por defecto de la hora actual
  updated_at = db.Column(db.DateTime, default=func.now())  # Columna timestamp con valor por defecto de la hora actual
  db.relationship('Address', backref='person', lazy=True)
