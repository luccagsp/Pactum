from db import db
from sqlalchemy.sql import func

class Reservation(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    eventhall_id = db.Column(db.Integer, db.ForeignKey('eventhall.id'), nullable=False, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reservation_date = db.Column(db.DateTime, nullable=False)
    hora_reserva = db.Column(db.DateTime, nullable=False)
    url_payment = db.Column(db.String(255))
    state = db.Column(db.String(50), default="Pendiente")
    reservation_price = db.Column(db.Integer)
    validated_by = db.Column(db.Integer)
    validated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now())
    deleted_at = db.Column(db.DateTime)

    # def validate_reserve( eventhall_id, client_id, reservation_date, hora_reserva):