from sqlalchemy.sql import func
from db import db, UserMixin

class Disponibilidad(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'), nullable=False)
    horarios = db.Column(db.JSON, nullable=False)
    creado_en = db.Column(db.DateTime, default=func.now())
    actualizado_en = db.Column(db.DateTime, default=func.now())