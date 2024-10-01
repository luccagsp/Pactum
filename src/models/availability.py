from sqlalchemy.sql import func
from db import db, UserMixin

class Availability(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    eventhall_id = db.Column(db.Integer, db.ForeignKey('eventhall.id'), nullable=False)
    hours = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now())