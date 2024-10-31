from db import db
from sqlalchemy.sql import func
from datetime import datetime
from config import regular_exps

class Reservation(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    eventhall_id = db.Column(db.Integer, db.ForeignKey('eventhall.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reservation_date = db.Column(db.Date, nullable=False)
    reservation_time = db.Column(db.Time, nullable=False)
    url_payment = db.Column(db.String(255))
    state = db.Column(db.String(50), default="pending")
    reservation_price = db.Column(db.Integer)
    validated_by = db.Column(db.Integer)
    validated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime)
    user = db.relationship('User', backref='reservations', lazy=True)

    @staticmethod
    def from_reserva(eventhall_id, user_id, reservation_date, reservation_time, url_payment=None, state="pending", reservation_price=int, validated_by=None, validated_at=None, deleted_at=None):
        # Validar si el precio es un número
        if not isinstance(reservation_price, int) and not int(reservation_price):
            return [False, "El precio solo puede conotener numeros"]
        if not isinstance(eventhall_id, int) and not int(eventhall_id):
            return [False, "La id del salon solo puede contener numeros"]
        if state != "pending" and state != "reserved":
            return [False, f"Estado '{state}', invalido. Debe ser: 'pending' o 'reserved"]
        
        # Asegurarse de que `reservation_date` y `reservation_time` sean objetos datetime
        if isinstance(reservation_date, str):
            try:
                reservation_date = datetime.strptime(reservation_date, '%Y-%m-%d').date()
            except ValueError:
                return [False, "Formato invalido en fecha de reserva, deberia de ser: 'YYYY-MM-DD'"]

        if isinstance(reservation_time, str):
            try:
                reservation_time = datetime.strptime(reservation_time, '%H:%M').time()
            except ValueError:
                return [False, "Formato invalido en hora de reserva, deberia de ser: 'HH:MM'"]
            
        if url_payment != None:
            if regular_exps.link.match(url_payment) == None:
                return [False, "url de imágen invalida"]

        # Crear el objeto Reservation
        return [True, Reservation(eventhall_id=eventhall_id, user_id=user_id, reservation_date=reservation_date, reservation_time=reservation_time, url_payment=url_payment, state=state, reservation_price=reservation_price, validated_by=validated_by, validated_at=validated_at, deleted_at=deleted_at)]