from db import db, UserMixin
from sqlalchemy.sql import func

class Reservation(db.Model, UserMixin):    
    id = db.Column(db.Integer, primary_key=True)
    eventhall_id = db.Column(db.Integer, db.ForeignKey('eventhall.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reservation_date = db.Column(db.DateTime, nullable=False)
    hora_reserva = db.Column(db.DateTime, nullable=False)
    url_payment = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(50), default="Pendiente")
    validated_by = db.Column(db.Integer)
    validated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now())
    deleted_at = db.Column(db.DateTime)