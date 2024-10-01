from db import db, UserMixin
from sqlalchemy.sql import func

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