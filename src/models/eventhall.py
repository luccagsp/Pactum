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
    place_number = db.Column(db.String(2200))
    alias = db.Column(db.String(200))
    deposit_price = db.Column(db.Integer, nullable=False)
    instant_booking  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=func.now())  # Columna timestamp con valor por defecto de la hora actual
    updated_at = db.Column(db.DateTime, default=func.now())  # Col
    db.relationship('availability', backref='person', lazy=True)
    images = db.relationship('Image', backref='eventhall')
    
    # user = db.relationship('User', back_populates='images')

    def validate_eventhall( owner_id,
                            name,
                            deposit_price,
                            alias = None,
                            instant_booking = False, 
                            description = None, 
                            street_address=None, 
                            place_number=None):
        # Verifica que no haya espacios al principio ni al final
        print(instant_booking)
        if not deposit_price:
            return [False, 'Falta deposit']
        if name != name.strip():
            return [False, "Error: invalid name"]
        # Expresión regular para verificar solo caracteres alfanuméricos y espacios
        if not regular_exps.name.match(name):
            return [False, "Error: invalid name"]
        if not int(deposit_price) or int(deposit_price) < 0:
            return [False, "Error: invalid deposit_price"]
        if not isinstance(instant_booking, bool):
            print(instant_booking)
            print(type(instant_booking))
            return [False, "Error: instant_booking must be boolean"]

        return [Eventhall(owner_id=owner_id,
                        name=name,
                        deposit_price=deposit_price, 
                        instant_booking=instant_booking, 
                        description=description, 
                        street_address=street_address, 
                        place_number=place_number,
                        alias=alias)]
