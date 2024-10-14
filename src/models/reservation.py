from db import db
from sqlalchemy.sql import func
import datetime
from config import regular_exps

class Reservation(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    eventhall_id = db.Column(db.Integer, db.ForeignKey('eventhall.id'), nullable=False, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reservation_date = db.Column(db.DateTime, nullable=False)
    hora_reserva = db.Column(db.DateTime, nullable=False)
    url_payment = db.Column(db.String(255))
    state = db.Column(db.String(50), default="pendiente")
    reservation_price = db.Column(db.Integer)
    validated_by = db.Column(db.Integer)
    validated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now())
    deleted_at = db.Column(db.DateTime)
    @staticmethod
    def from_reserva(eventhall_id, client_id, reservation_date, hora_reserva, url_payment=None, state="Pendiente", reservation_price=int, validated_by=None, validated_at=None, deleted_at=None):
        # Validar si el precio es un número
        if not isinstance(reservation_price, int):
            return ["price must contain only numbers"]
        if not isinstance(eventhall_id, int):
            return ["eventhall_id must contain only numbers"]
        if state != "Pendiente" and state != "Reservado":
            return ["invalid state"]


        # Asegurarse de que `reservation_date` y `hora_reserva` sean objetos datetime
        if isinstance(reservation_date, str):
            try:
                reservation_date = datetime.strptime(reservation_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return ["Invalid date format for reservation_date, should be 'YYYY-MM-DD HH:MM:SS'"]

        if isinstance(hora_reserva, str):
            try:
                hora_reserva = datetime.strptime(hora_reserva, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return ["Invalid date format for hora_reserva, should be 'YYYY-MM-DD HH:MM:SS'"]
            
        if regular_exps.link.match(url_payment) == None:
            return ["Invalid url"]

        # Crear el objeto Reservation
        return [None, Reservation(eventhall_id=eventhall_id, client_id=client_id, reservation_date=reservation_date, hora_reserva=hora_reserva, url_payment=url_payment, state=state, reservation_price=reservation_price, validated_by=validated_by, validated_at=validated_at, deleted_at=deleted_at)]