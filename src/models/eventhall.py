import config.regular_exps as regular_exps
from db import db
from sqlalchemy import JSON
from sqlalchemy.sql import func

class Eventhall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(2200))
    street_address = db.Column(db.String(80))
    street_number = db.Column(db.String(10))
    alias = db.Column(db.String(200), nullable=False)
    reservation_price = db.Column(db.Integer, nullable=False)
    instant_booking  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=func.now())  # Columna timestamp con valor por defecto de la hora actual
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())  # Col
    db.relationship('availability', backref='person', lazy=True)
    images = db.relationship('Image', backref='eventhall')
    
    # user = db.relationship('User', back_populates='images')

    def validate_eventhall( owner_id,name,reservation_price,alias = None,instant_booking = False, description = None, street_address=None, street_number=None):
        if not name: return [False, 'Falta nombre del salón']
        if not reservation_price:
            return [False, 'Falta precio de deposito']
        # Verifica que no haya espacios al principio ni al final
        instant_booking = bool(instant_booking)
        if alias == None:
            return [False, 'Falta alias']
        if not reservation_price:
            return [False, 'Falta precio de deposito']
        if name != name.strip():
            return [False, "Error: invalid name"]
        if len(name) > 50:
            return [False, "Nombre muy largo"]
        # Expresión regular para verificar solo caracteres alfanuméricos y espacios
        if not regular_exps.name.match(name):
            return [False, "El nombre no puede contener caracteres especiales"]
        if not int(reservation_price) or int(reservation_price) < 0:
            return [False, "Error: invalid reservation_price"]
        if description != None and len(description) > 2200:
            return [False, "Descripcion muy larga"]
        if not isinstance(instant_booking, bool):
            return [False, "'instant_booking' debe ser Booleano"]

        return [Eventhall(owner_id=owner_id,
                        name=name,
                        reservation_price=reservation_price, 
                        instant_booking=instant_booking, 
                        description=description, 
                        street_address=street_address, 
                        street_number=street_number,
                        alias=alias)]
